from pathlib import Path

import tomli
from manim import BLACK, WHITE

# ToDo – Do this properly
CONFIG = {
    "background": WHITE,
    "colour": BLACK,
    "pixelsPerUnit": 274,
    "runTime": 0.1,
}


def load(path: Path):
    with open(path, "rb") as f:
        data = tomli.load(f)
    CONFIG.update(**data)
