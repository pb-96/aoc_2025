from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Set, Callable
from functools import partial


@dataclass
class DayType:
    day_name: str

    def get_name(self):
        return self.day_name

    def part_one(self):
        raise NotImplementedError("Not Implemented")

    def part_two(self):
        raise NotImplementedError("Not Implemented")

    def both_parts(self, data: List[str]):
        raise NotImplementedError("Not Implemented")


def find_data_file(location: Path, day_name: str) -> List[str]:
    all_files = [
        f for f in location.iterdir() if f.name.endswith(".txt") and f.stem == day_name
    ]
    assert len(all_files) > 0, "Could not find data file"
    file_path = next(iter(all_files), None)
    assert file_path
    return file_path.read_text().splitlines()


class DisplayNode:
    def __init__(self, curr: str, children: List[str, "DisplayNode"] = []):
        self.curr = curr
        self.children = children

    def __repr__(self):
        return f"Root={self.curr}, children={self.children}"


def build_display_node(root: Path, predicate: Callable[[Path], bool]):
    given_root = DisplayNode(root, children=[])
    for child in root.iterdir():
        if child.is_file() and predicate(given_path=child):
            given_root.children.append(child)
        # Skips hidden folders
        elif child.is_dir() and predicate(given_path=child):
            given_root.children.append(build_display_node(child, predicate))
    return given_root


def parse_gitignore_file(gitignore_fp: Path) -> Tuple[Set, Set]:
    txt = gitignore_fp.read_text().splitlines()
    skip_dirs = set()
    skip_files = set()

    for t in txt:
        if not t:
            continue
        elif t.startswith("#"):
            continue
        elif t.startswith("/") or t.endswith("/"):
            skip_dirs.add(t.replace("/", ""))
        else:
            skip_files.add(t)
    return skip_dirs, skip_files


def predicate_path(
    given_path: Path, skip_on_dirs: Set[str], skip_on_files: Set[str]
) -> bool:
    if (
        given_path.is_dir()
        and not given_path.name.startswith(".")
        and given_path.name not in skip_on_dirs
    ):
        return True
    if given_path.is_file() and given_path.suffix not in skip_on_files:
        return True
    return False


def display_dir(root: Path, skip_on_dirs: Set[str], skip_on_files: Set[str]):
    "Utils wrapper to display files and data - helps with Readme's and passing context to an LLM -> this tech exists but wanted to write myself"
    predicate = partial(
        predicate_path, skip_on_dirs=skip_on_dirs, skip_on_files=skip_on_files
    )
    as_display_node = build_display_node(root, predicate)
    print(as_display_node)
