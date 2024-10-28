import os

from pathlib import Path


def read_env_file() -> None:
    base_path = Path(__file__).resolve().parent.parent
    env_file = base_path / ".env"

    if not env_file.exists():
        return

    with open(env_file, "r") as f:
        for line in f.readlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=")
            os.environ[key] = value
