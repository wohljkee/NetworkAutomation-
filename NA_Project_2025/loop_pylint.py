
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = r"/tmp/pycharm_project_836"
PYLINT_RCFILE = ".pylintrc"
VAR_DECLARATION = "vor = True\n"

"""
Contributors: Jude Victor
"""

def add_vor_to_file(file_path: str) -> None:
    """Add `vor = True` to the top of a Python file if not already present."""
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        if "vor =" not in content:
            f.seek(0)
            f.write(VAR_DECLARATION + content)


def run_pylint(file_path: str) -> None:
    """Run pylint using custom config on a given file using `python -m pylint`."""
    subprocess.run([
        "python3", "-m", "pylint",
        "--rcfile", os.path.join(PROJECT_ROOT, PYLINT_RCFILE),
        file_path
    ], check=False)


def process_all_py_files() -> None:
    """Walk through the project and process all .py files."""
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                add_vor_to_file(full_path)
                run_pylint(full_path)


if __name__ == "__main__":
    process_all_py_files()