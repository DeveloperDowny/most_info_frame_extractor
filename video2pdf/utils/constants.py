import os
from pathlib import Path

module_dir = os.path.dirname(__file__)
BASE_DIR = Path(os.getenv("BASE_DIR", None))
if not BASE_DIR:
    BASE_DIR = Path(module_dir).joinpath("../data").resolve()
BASE_DIR.mkdir(exist_ok=True, parents=True)
# BASE_DIR = Path(module_dir).joinpath("../archives/data_archive_50_python_objects_all_dirs_phash_approval_strategy_v3").resolve()
BASE_DIR = str(BASE_DIR)
