from viktor._vendor import libcst
import re

from pathlib import Path
from typing import List, Dict

from viktor._codemod.__main__ import _prompt_user, _patch_tree, _print_diff, _python_file_paths

_REQUIREMENTS = [
    'munch',
    'numpy',
    'requests',
    'pandas',
    'matplotlib'
]


def specific_fix(key_paths: Dict[str, Path], apply: bool, keep_original: bool, patched_files: list) -> None:

    used_dependencies = _get_used_dependencies(key_paths['app_dir'])
    if not used_dependencies:
        return

    if 'requirements_file' not in key_paths:
        raise FileNotFoundError("No file named 'requirements.txt' found")

    requirements_path = key_paths['requirements_file']
    rel_path = requirements_path.relative_to(key_paths['root_dir'])

    with open(requirements_path, 'r') as f:
        source_code = f.read()
    modified_code = _get_modified_code(requirements_path, used_dependencies)

    if source_code != modified_code:
        _print_diff(source_code, modified_code, rel_path)
        user_response = 'y' if apply else ''  # reset user input given for previous diff

        if not user_response:
            user_response = _prompt_user()

        if user_response == 'y':
            _patch_tree(source_code, modified_code, requirements_path, rel_path, keep_original)
            patched_files.append(rel_path)


def _get_used_dependencies(path: Path) -> List[str]:

    dependencies = set()
    for path_ in _python_file_paths(path):
        with open(path_, 'rb') as python_file:
            python_source = python_file.read()

        try:
            source_tree = libcst.parse_module(python_source)
            visitor = Visitor()
            source_tree.visit(visitor)
            dependencies = dependencies | visitor.used_dependencies
        except Exception:
            continue

    return list(dependencies)


def _get_modified_code(source_path: Path, used_dependencies: List[str]) -> str:

    requirement_versions = {
        'munch': '<3.0.0',
        'numpy': '<2.0.0',
        'requests': '<3.0.0',
        'pandas': '<2.0.0',
        'matplotlib': '<4.0.0'
    }
    requirements_to_be_added = {k_: v_ for k_, v_ in requirement_versions.items() if k_ in used_dependencies}

    modified_lines = []
    with open(source_path, 'r') as f:
        for line in f.readlines():

            for req in used_dependencies:
                if re.search(f'^\s*{req}', line):
                    del requirements_to_be_added[req]
                    continue

            modified_lines.append(line)

    # append remaining requirements
    for requirement, version in requirements_to_be_added.items():
        modified_lines.append(
            f'{requirement}{version}\n'
        )

    return ''.join(modified_lines)


class Visitor(libcst.CSTVisitor):

    def __init__(self):
        super().__init__()

        self.used_dependencies = set()

    def visit_ImportFrom(self, node: "ImportFrom"):
        req = node.module.value
        if req in _REQUIREMENTS:
            self.used_dependencies.add(req)

    def visit_Import(self, node: "Import"):
        for name in node.names:
            req = name.name.value
            if req in _REQUIREMENTS:
                self.used_dependencies.add(req)
