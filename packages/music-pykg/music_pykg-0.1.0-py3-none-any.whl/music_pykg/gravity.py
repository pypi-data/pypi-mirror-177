from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from scipy.io import FortranFile

if typing.TYPE_CHECKING:
    from typing import Dict

    import numpy as np


@dataclass(frozen=True)
class GravityFile:
    """Gravity profiles, read and/or written by the code

    See gravitation.f90
    """

    path: Path

    @cached_property
    def data(self) -> Dict[str, np.number]:
        ff = FortranFile(self.path, mode="r")
        (nr_tot,) = ff.read_record("int32")
        grav = ff.read_record("float64")
        ff.close()
        return {"NrTot": nr_tot, "grav": grav}
