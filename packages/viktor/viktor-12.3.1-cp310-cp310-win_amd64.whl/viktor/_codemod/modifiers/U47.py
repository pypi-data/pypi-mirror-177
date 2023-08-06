import re

from pathlib import Path
from typing import Dict

from viktor._codemod.__main__ import _prompt_user, _patch_tree, _print_diff


def specific_fix(key_paths: Dict[str, Path], apply: bool, keep_original: bool, patched_files: list) -> None:
    if 'manifest_file' not in key_paths:
        raise FileNotFoundError("No file named 'manifest.yml' found")

    manifest_path = key_paths['manifest_file']
    rel_path = manifest_path.relative_to(key_paths['root_dir'])

    with open(manifest_path, 'r') as f:
        source_code = f.read()
    modified_code = _get_modified_code(manifest_path)

    if source_code != modified_code:
        _print_diff(source_code, modified_code, rel_path)
        user_response = 'y' if apply else ''  # reset user input given for previous diff

        if not user_response:
            user_response = _prompt_user()

        if user_response == 'y':
            _patch_tree(source_code, modified_code, manifest_path, rel_path, keep_original)
            patched_files.append(rel_path)


def _get_modified_code(source_path: Path) -> str:
    modified_lines = []
    with open(source_path, 'r') as f:
        for line in f.readlines():
            if re.search('^\s*is_file\s*:', line):
                continue
            if re.search('^\s*preprocess_method\s*:', line):
                continue
            modified_lines.append(line)
    return ''.join(modified_lines)
