from __future__ import annotations

import copy
import json
import shlex
import shutil
import subprocess
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from .term import BlackHole, TermBase, err_msg, info_msg, warn_msg

if typing.TYPE_CHECKING:
    from typing import Dict, Iterator, Optional, Sequence

    from .dirs import TestsOutputDirectory

CMAKE_CACHE = "CMakeCache.txt"


class NoCacheFoundError(Exception):
    """Raised when automatic lookup of an existing cache failed."""

    pass


class Preset:
    """Preset and targets specification.

    If no target is provided, `music` will be listed.
    """

    def __init__(self, name: str, *targets: str):
        self.name = name
        self.targets = set(targets) if targets else {"music"}


class PresetCollection:
    """Opaque collection of presets."""

    def __init__(self, *presets: Preset):
        self._collection: Dict[str, Preset] = {}
        for preset in presets:
            self.add_preset(preset)

    def __iter__(self) -> Iterator[Preset]:
        return iter(self._collection.values())

    def __len__(self) -> int:
        return len(self._collection)

    def __bool__(self) -> bool:
        return bool(self._collection)

    def __contains__(self, preset: Preset) -> bool:
        built_preset = self._collection.get(preset.name, Preset("", ""))
        return (preset.targets).issubset(built_preset.targets)

    def add_preset(self, preset: Preset) -> None:
        """Add a preset to the collection."""
        if preset.name in self._collection:
            self._collection[preset.name].targets |= preset.targets
        else:
            self._collection[preset.name] = copy.deepcopy(preset)


class _PresetsConfig:
    """Preset configuration from CMakePresets.json."""

    def __init__(self, music_dir: Path):
        with (music_dir / "CMakePresets.json").open() as pjs:
            raw_presets = json.load(pjs)
        self._raw_presets = {}
        for item in raw_presets["configurePresets"]:
            name = item.pop("name")
            self._raw_presets[name] = item

    def preset_options(self, preset: Preset) -> Dict[str, str]:
        """Build options of given preset."""
        build_config = self._raw_presets[preset.name]
        opts = build_config.get("cacheVariables", {}).copy()
        parent_preset = build_config.get("inherits")
        if parent_preset is not None:
            parent_opts = self.preset_options(Preset(parent_preset))
            parent_opts.update(opts)
            opts = parent_opts
        return opts


def _curated_cache_copy(old: Path, new: Path) -> None:
    """Copy cache, removing undesired lines.

    The removed line is the one keeping track of the directory in which the
    cache was created.  This is fine to remove only this line and keep a lot of
    "INTERNAL" that shouldn't be copied in general since we are building the
    same code base and we aim at reproducing the build as closely as possible.
    """
    with old.open() as old_cache, new.open("w") as new_cache:
        for line in old_cache:
            if not line.startswith("CMAKE_CACHEFILE_DIR:INTERNAL"):
                new_cache.writelines([line])


@dataclass(frozen=True)
class BuildOutcome:
    """Result from calling CmakeBuilder.build_presets."""

    built_presets: PresetCollection
    all_successful: bool


@dataclass(frozen=True)
class CmakeBuilder:
    """Build binaries for tests using CMake.

    music_dir: the root of the music repository.
    cache_dir: an already existing build-tree whose CMake cache should be
        reused if necessary.
    """

    music_dir: Path
    outdir: TestsOutputDirectory
    requested_cache: Optional[Path] = None

    @cached_property
    def _config(self) -> _PresetsConfig:
        return _PresetsConfig(self.music_dir)

    @cached_property
    def _found_cache(self) -> Path:
        """Cache directory location."""
        if self.requested_cache is not None:
            return self.requested_cache
        build_dirs = ("build-debug", "bld-debug", "build", "bld")
        for build_dir in build_dirs:
            cache_dir = self.music_dir / build_dir
            if (cache_dir / CMAKE_CACHE).is_file():
                return cache_dir
        for cache_file in self.music_dir.glob(f"*/{CMAKE_CACHE}"):
            return cache_file.parent
        raise NoCacheFoundError

    def preset_tags(self, preset: Preset) -> Sequence[str]:
        """Tags related to build options."""
        opts = self._config.preset_options(preset)
        return [
            opts["dims"].replace(".", "_"),
            *preset.targets,
        ]

    def _configure_preset(self, preset: Preset, generator: str) -> None:
        sdir = self.music_dir
        bdir = self.outdir.build_path(preset)
        cmd = f"cmake --preset={preset.name} -S '{sdir}' -B '{bdir}' -G '{generator}'"
        subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            check=True,
        )

    def _get_generator(self, cache_file: Path) -> str:
        with cache_file.open() as cache:
            for line in cache:
                if line.startswith("CMAKE_GENERATOR:"):
                    return line.split("=", 1)[1].strip()
        return "Unix Makefiles"

    def build_presets(
        self,
        presets: PresetCollection,
        *,
        output_to: Optional[TermBase] = None,
        indent: int = 0,
    ) -> BuildOutcome:
        """Build test presets if necessary."""
        if not presets:
            return BuildOutcome(PresetCollection(), all_successful=True)
        output_to = output_to if output_to is not None else BlackHole()

        cache = self.outdir.builds_path / "cache.cmake"
        if cache.is_file() and self.requested_cache is not None:
            warn_msg(
                "Explicit cache location requested with `-c|--cache-from` is",
                "ignored as a cache already exists and `--keep` was passed",
            ).print_to(output_to, indent)
        if not cache.is_file():
            if self.requested_cache is None:
                warn_msg(
                    f"Found cache in existing build-tree {self._found_cache}",
                    "Use `-c|--cache-from <path>` to request a specific tree",
                ).print_to(output_to, indent)
            else:
                info_msg(
                    f"Using cache in existing build-tree {self._found_cache}"
                ).print_to(output_to, indent)
            _curated_cache_copy(self._found_cache / CMAKE_CACHE, cache)

        npresets = len(presets)
        ilen = len(str(npresets))
        build_success = True
        built_presets = PresetCollection()
        generator = self._get_generator(cache)
        for i, preset in enumerate(presets, 1):
            info_msg(
                f"Building preset {i:{ilen}}/{npresets}: {preset.name} {preset.targets!r}"
            ).print_to(output_to, indent)
            preset_dir = self.outdir.build_path(preset)
            preset_dir.mkdir(exist_ok=True)
            preset_cache = preset_dir / CMAKE_CACHE
            if not preset_cache.is_file():
                shutil.copy(cache, preset_cache)
            self._configure_preset(preset, generator)
            for tgt in preset.targets:
                build_log = preset_dir / f"build_{tgt}.log"
                with build_log.open("w") as blog:
                    bld_process = subprocess.run(
                        shlex.split(f"cmake --build '{preset_dir}' --target {tgt} -j"),
                        stdout=blog,
                        stderr=blog,
                    )
                if bld_process.returncode == 0:
                    built_presets.add_preset(Preset(preset.name, tgt))
                else:
                    build_success = False
                    err_msg(
                        f"Build of target `{tgt}` failed", f"See log in {build_log}"
                    ).print_to(output_to, indent + 1)
        return BuildOutcome(built_presets, build_success)
