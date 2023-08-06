from __future__ import annotations

import shutil
import typing
from dataclasses import dataclass
from pathlib import Path

from .source_tree import MusicSourceTree
from .test import ConcreteTest

if typing.TYPE_CHECKING:
    from .cmake_builder import Preset


@dataclass(frozen=True)
class TestRunDirectory:
    test: ConcreteTest
    path: Path
    build_path: Path

    @property
    def _run_tag_path(self) -> Path:
        return self.path / "run_successful.tag"

    def is_ready(self) -> bool:
        return self._run_tag_path.is_file()

    def run(self, verbose: bool = False) -> None:
        # Start with fresh run directory
        shutil.rmtree(self.path, ignore_errors=True)
        self.path.mkdir(parents=True)

        # Setup files required for run, coming from
        # ... the build
        for tgt in self.test.build_preset.targets:
            # hardlink here enables BuildCheckStage to verify
            # whether the build artefacts changed
            (self.build_path / tgt).link_to(self.path / tgt)
        # ... the test problem
        self.test.setup_dir_for_run(self.path)

        # Run the test
        self.test.run_in_dir(self.path, verbose=verbose)

        # Touch the run successful flag
        self._run_tag_path.touch()


@dataclass(frozen=True)
class TestsOutputDirectory:
    music_tree: MusicSourceTree
    path: Path

    def prepare(self, wipe: bool = True) -> None:
        if wipe and self.path.is_dir():
            shutil.rmtree(self.path)
        self.builds_path.mkdir(parents=True, exist_ok=True)

        # Capture VCS revision and diff
        self.music_tree.store_vcs_info(
            vcs_head_fname=self.path / "git_head.log",
            vcs_diff_fname=self.path / "git_diff.log",
        )

    @property
    def builds_path(self) -> Path:
        """Location of preset builds."""
        return self.path / "builds"

    def build_path(self, preset: Preset) -> Path:
        """Location of a given preset build, a subdirectory of :attr:`builds_path`."""
        return self.builds_path / preset.name

    def run_path(self, test: ConcreteTest) -> Path:
        """Location of the run for a given path."""
        return self.path / "runs" / test.name

    def test_run_directory(self, test: ConcreteTest) -> TestRunDirectory:
        return TestRunDirectory(
            test=test,
            path=self.run_path(test),
            build_path=self.build_path(test.build_preset),
        )
