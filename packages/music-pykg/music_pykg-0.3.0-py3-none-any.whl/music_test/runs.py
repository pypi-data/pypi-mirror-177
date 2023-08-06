from __future__ import annotations

import shlex
import shutil
import subprocess
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from music_pykg.namelist import MusicNamelist

from .dumps import FileDump
from .utils import check_call_tee

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import ClassVar, Optional, Sequence, Tuple


class TestRunException(Exception):
    """Base exception for test errors"""


class TestRequiredFileNotFound(TestRunException):
    """File required for test run was not found"""


class TestExecutionError(TestRunException):
    """Test execution command failed"""


class Run(ABC):
    @property
    def run_log_filename(self) -> str:
        return "run.log"

    @abstractmethod
    def command(self, run_path: Path) -> str:
        """Command to run."""

    def execute(self, run_path: Path, verbose: bool = False) -> None:
        """Execute the run in the selected `run_path`"""
        run_log = run_path / self.run_log_filename
        with open(run_log, "w") as run_log_file:
            try:
                check_call_tee(
                    shlex.split(self.command(run_path)),
                    run_log_file,
                    also_to_stdout=verbose,
                    cwd=run_path,
                )
            except subprocess.CalledProcessError as err:
                raise TestExecutionError(f"Run command error, check '{run_log}': {err}")

    @abstractmethod
    def setup_run_dir_from_template(self, src_path: Path, dst_path: Path) -> None:
        """Copy run-specific files located at `src_path` into `dst_path`"""
        raise NotImplementedError()

    @abstractmethod
    def auto_tags(self, path: Path) -> Sequence[str]:
        """Return a sequence of automatic tags determined from the run properties."""
        raise NotImplementedError()


@dataclass(frozen=True)
class BareCmd(Run):
    cmd: str

    def command(self, run_path: Path) -> str:
        return self.cmd

    def setup_run_dir_from_template(self, src_path: Path, dst_path: Path) -> None:
        pass

    def auto_tags(self, path: Path) -> Sequence[str]:
        return ()


@dataclass(frozen=True)
class ConvertCmd(Run):
    namelist: str
    model1d: str
    extra_files: Tuple[str, ...] = ()

    def command(self, run_path: Path) -> str:
        return f"./convert {self.namelist}"

    def setup_run_dir_from_template(self, src_path: Path, dst_path: Path) -> None:
        for filename in (self.model1d, self.namelist):
            shutil.copy(src_path / filename, dst_path)
        for filename in self.extra_files:
            shutil.copy(src_path / filename, dst_path)

    def auto_tags(self, path: Path) -> Sequence[str]:
        return ()


@dataclass(frozen=True)
class MusicRun(Run):
    """A (serial or parallel) run of MUSIC.

    The number of cores to run on is obtained from the namelist.
    """

    namelist: str
    start_dump: FileDump
    extra_required_files: Tuple[str, ...] = ()
    binary: str = "./music"
    skip_self_tests: Optional[bool] = None
    skip_self_tests_dflt: ClassVar[bool] = True

    def __post_init__(self) -> None:
        if self.skip_self_tests is None:
            object.__setattr__(self, "skip_self_tests", self.skip_self_tests_dflt)

    def command(self, run_path: Path) -> str:
        nprocs = MusicNamelist(run_path / self.namelist).num_procs
        opts = "--skip-self-tests" if self.skip_self_tests else ""
        return f"mpirun -np {nprocs} '{self.binary}' '{self.namelist}' {opts}"

    def setup_run_dir_from_template(self, src_path: Path, dst_path: Path) -> None:
        # Create directory for output files; important otherwise MUSIC crashes weirdly
        (dst_path / "output").mkdir()

        # Copy namelist and initial dump
        shutil.copy(src_path / self.namelist, dst_path)
        shutil.copy(src_path / self.start_dump.filename, dst_path)

        # Copy any extra required files
        for fname in self.extra_required_files:
            shutil.copy(src_path / fname, dst_path)

    def auto_tags(self, path: Path) -> Sequence[str]:
        namelist = MusicNamelist(path / self.namelist)

        # Serial/parallel run
        tags = ["serial" if namelist.num_procs == 1 else "parallel"]

        # EoS
        tags += [namelist.eos + "_eos"]

        # Geometry
        if namelist.is_cartesian:
            tags += ["cart"]

        # Scalars
        if namelist.nscalars > 0:
            tags += ["scalars"]

        if namelist.nactive_scalars > 0:
            tags += ["activescalars"]

        if namelist.has_rotation:
            tags += ["rot"]

        if namelist.mhd_enabled:
            tags += ["mhd"]

        # Gravity
        def gravity_tags() -> Sequence[str]:
            # Mind the order of those, see gravitation.f90
            if namelist.gravity_file.strip() != "":
                return ["gravity_external"]

            if namelist.consistent_gravity:
                return ["gravity_from_hse"]

            if namelist.gravity < 0:
                return ["gravity_mass_shells"]

            if namelist.gravity > 0:
                return ["gravity_const"]

            return ["gravity_none"]

        tags += gravity_tags()

        return tags
