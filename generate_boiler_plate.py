from datetime import datetime

NUMBER_TO_WORD = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
}


def number_to_word(n: int) -> str:
    return NUMBER_TO_WORD.get(n, f"Day{n}")


BOILER_PLATE = """
from data_loader import DayType
from typing import List

class Day{number_name}(DayType):
    day_name: str = "{day_number}"

    def part_one(self, data: List[str]):
        return 0

    def part_two(self, data: List[str]):
        return 0

"""


def generate_boiler_plate_string(current_date: datetime) -> str:
    day_number = current_date.day
    day_string = f"day{day_number:02d}"
    number_name = number_to_word(day_number)
    return BOILER_PLATE.format(number_name=number_name, day_number=day_string)


def generate_init_file_string(current_date: datetime) -> str:
    date_range = range(1, current_date.day + 1)
    cls_names = [number_to_word(n) for n in date_range]
    as_cls_names = [f"Day{cls_name}" for cls_name in cls_names]

    import_string = ""

    for day_int, cls_name in zip(date_range, as_cls_names):
        this_day_string = f"day{day_int:02d}"
        import_string += f"from aoc{current_date.year}.{this_day_string}.{this_day_string} import {cls_name}\n"

    import_string += "\n\n"

    all_string = "__all__ = [\n"
    for cls_name in as_cls_names:
        all_string += f"\t'{cls_name}',\n"

    all_string += "]\n"

    return import_string + all_string
