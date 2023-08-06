from __future__ import annotations

import typing
import warnings
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import numpy as np
from scipy.io import FortranFile

if typing.TYPE_CHECKING:
    from os import PathLike
    from typing import (
        Any,
        Callable,
        Dict,
        Generator,
        Literal,
        Mapping,
        Sequence,
        Set,
        Tuple,
        Union,
    )

    Dtype = Union[str, np.dtype]
    FileName = Union[str, PathLike]
    HeaderDict = Dict[str, Any]
    DataDict = Dict[str, np.ndarray]
    TocDict = Dict[str, LogFileArrayRecord]


@dataclass(frozen=True)
class MusicDumpInfo:
    num_space_dims: int
    num_velocities: int
    num_scalars: int
    dtype_real: np.dtype = np.dtype("float64")
    dtype_int: np.dtype = np.dtype("int32")


@dataclass(frozen=True)
class LogFileArrayRecord:
    log_file: MusicLogFile
    name: str
    data_pos: int
    dtype: Dtype
    squeeze: bool = True

    def read(self) -> np.ndarray:
        self.log_file.seek(self.data_pos)
        return self.log_file._read_array_data(self.dtype, self.squeeze)


class MusicLogFile:
    def __init__(self, file_name: FileName, mode: str = "rb", int_t: Dtype = "int32"):
        self.f = open(file_name, mode)
        self.file_size = Path(file_name).stat().st_size
        self.int_t = int_t

    def close(self) -> None:
        self.f.close()

    def __del__(self) -> None:
        self.close()

    def seek(self, pos: int) -> None:
        self.f.seek(pos)

    def tell(self) -> int:
        return self.f.tell()

    def seek_start(self) -> None:
        self.seek(0)

    def at_eof(self) -> bool:
        return self.f.tell() >= self.file_size

    def read(self, dtype: Dtype, count: int) -> np.ndarray:
        return np.fromfile(self.f, dtype=dtype, count=count).squeeze()

    def _read_name_record(self) -> str:
        # NameRecord:
        #   size     int32[1]
        #   chars    char[size]
        length = int(self.read(self.int_t, 1))
        name_bytes = self.f.read(length)
        return name_bytes.decode(encoding="ascii")

    def _read_type_record(self) -> np.ndarray:
        # TypeRecord:
        #   type     char[1]
        return self.read("byte", 1)

    def _read_data_record(self, dtype: Dtype, count: int) -> np.ndarray:
        return self.read(dtype, count).squeeze()

    def _skip_data_record(self, dtype: Dtype, count: int) -> None:
        self.seek(self.tell() + np.dtype(dtype).itemsize * count)

    def read_scalar(self, dtype: Dtype) -> Tuple[str, np.ndarray]:
        # ScalarItem:
        #   NameRecord
        #   TypeRecord
        #   DataRecord
        name = self._read_name_record()
        _ = self._read_type_record()
        scalar = self._read_data_record(dtype, 1)
        return name, scalar

    def read_named_scalar(self, name: str, dtype: Dtype) -> np.ndarray:
        name2, scalar = self.read_scalar(dtype)
        if name != name2:
            raise ValueError(f"invalid log item name, expected '{name}', got '{name2}'")
        return scalar

    def _read_transpose_record_as_order(self) -> Literal["C", "F"]:
        # TransposeRecord:
        #   flag     char[1]
        flag = int(self.read("byte", 1))
        assert flag in [0, 1]
        if flag == 0:
            return "C"
        else:
            return "F"

    def _read_dims_record(self) -> np.ndarray:
        # DimsRecord:
        #   dims     int32[3]
        return self.read(self.int_t, 3)

    def _read_array_data(self, dtype: Dtype, squeeze: bool = True) -> np.ndarray:
        # ArrayDataItem
        #   TypeRecord
        #   TransposeRecord
        #   DimsRecord
        #   DataRecord
        _ = self._read_type_record()
        order = self._read_transpose_record_as_order()
        dims = self._read_dims_record()
        array = self._read_data_record(dtype, np.product(dims))
        array = array.reshape(dims, order=order)
        if squeeze:
            array = array.squeeze()
        return array

    def _skip_array_data(self, dtype: Dtype) -> None:
        _ = self._read_type_record()
        _ = self._read_transpose_record_as_order()
        dims = self._read_dims_record()
        self._skip_data_record(dtype, np.product(dims))

    def read_array(self, dtype: Dtype, squeeze: bool = True) -> Tuple[str, np.ndarray]:
        # ArrayItem:
        #   NameRecord
        #   ArrayDataItem
        name = self._read_name_record()
        return name, self._read_array_data(dtype, squeeze)

    def read_lazy_array(
        self,
        dtype: Dtype,
        squeeze: bool = True,
    ) -> LogFileArrayRecord:
        # ArrayItem:
        #   NameRecord
        #   ArrayDataItem
        name = self._read_name_record()
        lazy_array = LogFileArrayRecord(self, name, self.tell(), dtype, squeeze)
        self._skip_array_data(dtype)
        return lazy_array

    def read_named_array(
        self, name: str, dtype: Dtype, squeeze: bool = True
    ) -> np.ndarray:
        name2, array = self.read_array(dtype, squeeze)
        if name != name2:
            raise ValueError(f"invalid log item name, expected '{name}', got '{name2}'")
        return array


class MusicNewFormatDumpFile:
    """See readwrite_new_format.90:read_new_model_helium{2d,3d}"""

    header_string = "MUSIC Log File version 1.2"

    def __init__(
        self,
        file_name: FileName,
        dump_info: MusicDumpInfo,
        keep_field: Callable[[str], bool] = lambda s: True,
    ):
        self.file_name = file_name
        self.dump_info = dump_info
        self.real_t = dump_info.dtype_real
        self.int_t = dump_info.dtype_int
        self.keep_field = keep_field

    @property
    def _field_names_axes(self) -> Sequence[str]:
        ndim = self.dump_info.num_space_dims
        return ["r", "theta", "phi"][:ndim]

    def _read_header(self, f: MusicLogFile) -> HeaderDict:
        f.seek_start()
        header_size = f.read(self.int_t, 1)
        if header_size != len(self.header_string):
            warnings.warn(
                f"MUSIC header size mismatch in {self.file_name}, "
                f"expected {len(self.header_string)}, got {header_size}. "
                "File might be damaged. Trying to read anyway."
            )

        f.read("byte", len(self.header_string))

        xmcore = f.read_named_scalar("xmcore", self.real_t)
        model = f.read_named_scalar("model", self.int_t)
        dtn = f.read_named_scalar("dtn", self.real_t)
        time = f.read_named_scalar("time", self.real_t)

        nfaces = f.read_named_array("dims", self.int_t)

        num_ghost = f.read_named_scalar("num_ghost", self.int_t)
        geometry = f.read_named_scalar("geometry", self.int_t)
        eos = f.read_named_scalar("eos", self.int_t)
        if eos == 0:
            gamma = f.read_named_scalar("gamma", self.real_t)
        else:
            gamma = None
        ikap = f.read_named_scalar("ikap", self.int_t)
        yy = f.read_named_scalar("Y", self.real_t)
        zz = f.read_named_scalar("Z", self.real_t)

        # this should be a dataclass
        header = dict(
            xmcore=xmcore,
            model=model,
            nfaces=nfaces,
            num_ghost=num_ghost,
            eos=eos,
            gamma=gamma,
            ikap=ikap,
            Y=yy,
            Z=zz,
            geometry=int(geometry),
            dtn=float(dtn),
            time=float(time),
        )

        # Read grid locations along axes
        for iax, axname in enumerate(self._field_names_axes, 1):
            header[f"face_loc_{iax}"] = f.read_named_array(axname, self.real_t)

        return header

    def _read_header_and_toc(self, f: MusicLogFile) -> Tuple[HeaderDict, TocDict]:
        header = self._read_header(f)

        def gen_toc() -> Generator[LogFileArrayRecord, None, None]:
            seen: Set[str] = set()
            while not f.at_eof():
                toc_entry = f.read_lazy_array(self.real_t)
                assert (
                    toc_entry.name not in seen
                ), "Duplicate entries for field '{toc_entry.name}' in file '{self.file_name}'"
                seen.add(toc_entry.name)
                if self.keep_field(toc_entry.name):
                    yield toc_entry

        return header, dict([(toc_entry.name, toc_entry) for toc_entry in gen_toc()])

    def read(self) -> Tuple[HeaderDict, DataDict]:
        f = MusicLogFile(self.file_name, int_t=self.int_t)
        header, toc = self._read_header_and_toc(f)
        data = {name: toc_entry.read() for name, toc_entry in toc.items()}
        f.close()
        return header, data

    def write(self, data: Mapping[str, Any]) -> None:
        writer = _MusicNewFormatDumpWriter(self.file_name, self.dump_info)
        writer.write(data)
        writer.close()

    def read_header(self) -> HeaderDict:
        f = MusicLogFile(self.file_name, int_t=self.int_t)
        header = self._read_header(f)
        f.close()
        return header

    @cached_property
    def field_names(self) -> Sequence[str]:
        f = MusicLogFile(self.file_name, int_t=self.int_t)
        _, toc = self._read_header_and_toc(f)
        f.close()
        return list(toc.keys())

    def keeping_only(self, keep: Callable[[str], bool]) -> MusicNewFormatDumpFile:
        return MusicNewFormatDumpFile(
            self.file_name,
            self.dump_info,
            keep_field=lambda field: self.keep_field(field) and keep(field),
        )


def shape3(shape: Sequence[int], fill_value: int = 1) -> Tuple[int, int, int]:
    shape = tuple(shape)
    # TYPE SAFETY: length of returned tuple is guaranteed to be three
    assert len(shape) <= 3
    return tuple(shape) + (3 - len(shape)) * (fill_value,)  # type: ignore


class _MusicNewFormatDumpWriter:
    """
    A quick and dirty implementation of dump file writing,
    initially written for the Stellar Hydro Days code comparison project.

    This class is meant for internal use only to this `io` module.
    Currently, it's bad OO design, as it cares about too many things:

     * the details of low-level storage (this should be delegated to MusicLogFile)

     * the sequence of records in the dump (this should be in MusicNewFormatDumpFile)

    Ideally this class should be split and integrated between MusicLogFile and MusicNewFormatDumpFile,
    but for now at least MusicNewFormatDumpFile works and provides a clean interface to the outside world.
    """

    def __init__(self, fname: Union[str, PathLike], dump_info: MusicDumpInfo):
        self.fd = open(fname, "wb")
        self.dump_info = dump_info

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        self.fd.close()

    def write(self, data: Mapping[str, Any]) -> None:
        # Magic header
        self.write_rawarr(np.array([26], dtype="int32"))
        self.write_rawstr("MUSIC Log File version 1.2")

        # Header data
        self.write_double("xmcore", data["xmcore"])
        self.write_int("model", data["model"])
        self.write_double("dtn", data["dtn"])
        self.write_double("time", data["time"])
        self.write_nfaces(data["nfaces"])
        self.write_int("num_ghost", data["num_ghost"])
        self.write_int("geometry", data["geometry"])
        self.write_int("eos", data["eos"])
        if data["eos"] == 0:
            self.write_double("gamma", data["gamma"])
        self.write_int("ikap", data["ikap"])
        self.write_double("Y", data["Y"])
        self.write_double("Z", data["Z"])

        # Grid
        self.write_gridarr("r", data["face_loc_1"])
        self.write_gridarr("theta", data["face_loc_2"])
        if self.dump_info.num_space_dims == 3:
            self.write_gridarr("phi", data["face_loc_3"])

        # Variables
        self.write_cube("rho", data["rho"])
        self.write_cube("e", data["e"])
        self.write_cube("v_r", data["v_r"])
        self.write_cube("v_t", data["v_t"])
        if self.dump_info.num_velocities == 3:
            self.write_cube("v_p", data["v_p"])

        # Scalars
        for i in range(1, self.dump_info.num_scalars + 1):
            self.write_cube(f"Scalar{i}", data[f"Scalar{i}"])

    def write_rawarr(self, arr: np.ndarray) -> None:
        self.fd.write(arr.tobytes(order="F"))

    def write_rawbytes(self, b: Sequence[int]) -> None:
        self.write_rawarr(np.array(b, dtype="byte"))

    def write_rawstr(self, s: str) -> None:
        self.fd.write(s.encode("ascii"))

    def write_nametag(self, name: str) -> None:
        self.fd.write(np.array(len(name), dtype="int32").tobytes())
        self.fd.write(name.encode("ascii"))

    def write_double(self, name: str, x: float) -> None:
        x_arr = np.array(x, dtype="float64")
        assert x_arr.size == 1
        self.write_nametag(name)
        self.write_rawbytes([2])
        self.write_rawarr(x_arr)

    def write_int(self, name: str, x: int) -> None:
        x_arr = np.array(x, dtype="int32")
        assert x_arr.size == 1
        self.write_nametag(name)
        self.write_rawbytes([0])
        self.write_rawarr(x_arr)

    def write_nfaces(self, dims: Tuple[int, ...]) -> None:
        self.write_nametag("dims")
        self.write_rawbytes([4, 0])
        self.write_rawarr(np.array([3, 1, 1], dtype="int32"))
        # fill_value=2 here since we have 2 faces along nonexistent dimensions
        self.write_rawarr(np.array(shape3(dims, fill_value=2), dtype="int32"))

    def write_gridarr(self, name: str, arr: np.ndarray) -> None:
        self.write_nametag(name)
        self.write_rawbytes([6, 0])
        self.write_rawarr(np.array([len(arr), 1, 1], dtype="int32"))
        self.write_rawarr(arr.astype("float64"))

    def write_cube(self, name: str, cube: np.ndarray) -> None:
        self.write_nametag(name)
        self.write_rawbytes([6, 1])
        self.write_rawarr(np.array(shape3(cube.shape, fill_value=1), dtype="int32"))
        self.write_rawarr(cube.astype("float64"))


class GravityFile:
    def __init__(self, fname: Union[str, PathLike]):
        self.fname = fname

    def write(self, data: Mapping[str, Any]) -> None:
        f = FortranFile(self.fname, "w")
        f.write_record(np.array([data["nr"]], dtype="int32"))
        f.write_record(np.array(data["g_r"], dtype="float64"))
        f.close()
