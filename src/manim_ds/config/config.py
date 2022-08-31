from pathlib import Path

import tomli

_DEFAULT_CONFIG_PATH = Path(__file__).parent / "default_config.toml"
CONFIG = {}


def load(path: Path):
    with open(path, "rb") as f:
        data = tomli.load(f)
    CONFIG.update(**data)


load(_DEFAULT_CONFIG_PATH)
