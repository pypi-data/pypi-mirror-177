from __future__ import annotations

import typing
from dataclasses import dataclass

from .cmake_builder import Preset

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional, Sequence

    from .comparison_checks import ComparisonCheck
    from .runs import Run
    from .self_checks import SelfCheck


@dataclass(frozen=True)
class Test:
    """A test to run"""

    build_preset: Preset
    run: Run
    self_check: Optional[SelfCheck]
    comparison_check: Optional[ComparisonCheck]
    description: str
    tags: Sequence[str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "tags", tuple(self.tags))
        if isinstance(self.build_preset, str):
            object.__setattr__(self, "build_preset", Preset(self.build_preset))


@dataclass(frozen=True)
class ConcreteTest(Test):
    name: str
    path: Path

    def setup_dir_for_run(self, dst_path: Path) -> None:
        """Setup given path for this test's run"""
        self.run.setup_run_dir_from_template(self.path, dst_path)

    def run_in_dir(self, path: Path, verbose: bool) -> None:
        self.run.execute(path, verbose=verbose)
