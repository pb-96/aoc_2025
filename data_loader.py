from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class DayType:
    day_name: str = "day0"

    def get_name(self):
        return self.day_name
    
    def part_one(self):
        raise NotImplementedError("Not Implemented")

    def part_two(self):
        raise NotImplementedError("Not Implemented")

    def both_parts(self, data: List[str]):
        raise NotImplementedError("Not Implemented")

def find_data_file(location: Path) -> List[str] | None:
    day_name = location.stem
    all_files = [f for f in location.iterdir() if f.name.endswith(".txt") and f.stem == day_name]
    assert len(all_files) > 0, "Could not find data file"
    file_path = next(iter(all_files), None)
    assert file_path
    return file_path.read_text().splitlines()
    

def display_dir(self):
    ...