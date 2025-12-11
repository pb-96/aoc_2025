from data_loader import DayType
from typing import List
from functools import cache


class DayEleven(DayType):
    day_name: str = "day11"

    def parse_data(self, data: List[str]):
        E = {}
        for line in data:
            x, ys = line.split(":")
            ys = ys.split()
            E[x] = ys
        self.E = E
        return E

    def part_one(self, data: List[str]):
        self.parse_data(data)
        return rec_p_one("you", self)

    def part_two(self, data: List[str]):
        self.parse_data(data)
        return rec_p_two("svr", False, False, self)

    def __hash__(self):
        return hash(f"{self.day_name}_at_{id(self)}")


@cache
def rec_p_one(x: str, cls: DayEleven) -> int:
    if x == "out":
        return 1
    else:
        return sum(rec_p_one(y, cls) for y in cls.E[x])


@cache
def rec_p_two(x: str, seen_dac: bool, seen_fft: bool, cls: DayEleven) -> int:
    if x == "out":
        return 1 if seen_dac and seen_fft else 0
    else:
        ans = 0
        for y in cls.E[x]:
            dac = seen_dac or y == "dac"
            fit = seen_fft or y == "fft"
            ans += rec_p_two(y, dac, fit, cls)
        return ans
