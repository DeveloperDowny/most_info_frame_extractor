import os
from pathlib import Path

# Use current working directory instead of module directory
# TODO: Use pydantic_settings in the future
BASE_DIR = os.getenv("BASE_DIR", None)
if not BASE_DIR:
    # Use current working directory where the CLI is run from
    BASE_DIR = Path.cwd().joinpath("data").resolve()
else:
    BASE_DIR = Path(BASE_DIR)
BASE_DIR.mkdir(exist_ok=True, parents=True)
BASE_DIR = str(BASE_DIR)