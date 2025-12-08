from data_loader import DayType
from typing import List
from collections import defaultdict
from math import prod


class DaySix(DayType):
    day_name: str = "day06"

    def apply_op(self, op: str, values: list[int]) -> int:
        """Apply + (sum) or * (product) to a list of values."""
        return sum(values) if op == "+" else prod(values)

    def parse_data_p1(self, data: list[str]):
        *rows, ops_line = data
        ops = ops_line.split()

        columns = defaultdict(list)
        for row in rows:
            for col_idx, val in enumerate(row.split()):
                columns[col_idx].append(int(val))

        return columns, ops

    def parse_data_p2(self, data: list[str]):
        *rows, ops_line = data
        delims = [i for i, c in enumerate(ops_line) if c in "*+"]
        ops = [c for c in ops_line if c in "*+"]
        delims.append(len(ops_line) + 1)
        chunks_by_row = [
            [
                list(row[start : delims[i + 1] - 1].replace(" ", "0"))
                for i, start in enumerate(delims[:-1])
            ]
            for row in rows
        ]
        columns = list(zip(*chunks_by_row))
        return zip(columns, ops)

    def part_one(self, data: List[str]):
        columns, ops = self.parse_data_p1(data)
        return sum(self.apply_op(ops[idx], vals) for idx, vals in columns.items())

    def part_two(self, data: List[str]):
        total = 0
        for cols, op in self.parse_data_p2(data):
            digit_buckets = defaultdict(list)
            for col in cols:
                for idx in range(len(col) - 1, -1, -1):
                    if col[idx] != "0":
                        digit_buckets[idx].append(col[idx])

            numbers = [int("".join(digits)) for digits in digit_buckets.values()]
            total += self.apply_op(op, numbers)
        return total
