from pathlib import Path
from typing import Dict

def specific_fix(key_paths: Dict[str, Path], apply: bool, keep_original: bool, patched_files: list) -> None: ...
