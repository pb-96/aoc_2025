from data_loader import DayType
from typing import List


class DayThree(DayType):
    day_name: str = "day03"

    def windows_gen(self, row: str):
        for i in range(0, len(row) - 1):
            it = iter(int(x) for x in row[i:])
            yield next(it), it

    def part_one(self, data: List[str]):
        maxes = {}
        for idx, row in enumerate(data):
            maxes[idx] = 0

            for first, it in self.windows_gen(row):
                as_num = first * 10 + max([*it])
                maxes[idx] = max(maxes[idx], as_num)

        return sum(maxes.values())

    def distinct_in_order(self, digits: str, k: int = 12) -> int:
        n = len(digits)
        to_remove = n - k

        stack = []

        for digit in map(int, digits):
            while stack and stack[-1] < digit and to_remove > 0:
                stack.pop()
                to_remove -= 1
            stack.append(digit)

        return int("".join(map(str, stack[:k])))

    def part_two(self, data: List[str]):
        total = 0
        for row in data:
            total += self.distinct_in_order(row)
        return total
