"""
Some utilities to use in several modules
"""
from typing import List
from pathlib import Path, PosixPath


def retrieve_current_dir() -> List[str]:
    """Static method that would check all the files inside the given directory where
    the user run the script, only keeping those that have a .py extension or the folder."""
    def __format_path(path: PosixPath) -> str:
        """Local function to format a path to a string"""
        return str(path).rsplit('/', maxsplit=1)[-1]

    # First, retrieve the absolute path where we run the script
    abs_path = Path().absolute()
    # From this absolute path, obtain the files for the directory
    all_files = []
    for _file in abs_path.iterdir():
        # If it is a .py file
        if str(_file).endswith('.py'):
            all_files.append(__format_path(_file))
        # If it is a directory but not a private one
        elif _file.is_dir() and not __format_path(_file).startswith('.'):
            all_files.append(__format_path(_file))
    # Return the list of files
    return all_files


def find_code(start_line: int, end_line: int | None, abs_path: str) -> str:
    """Find bad code from a given line and end lines."""
    with open(abs_path, 'r') as code_file:
        code = code_file.readlines()
    # From here, only return the lines that matter as a single multiline
    if start_line and end_line != start_line:
        return '\n'.join(c for c in code[start_line-1:end_line-1])[:-1]
    # If you don't have end_line
    return code[start_line-1][:-1]
