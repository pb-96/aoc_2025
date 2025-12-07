from data_loader import DayType
from typing import List
from collections import defaultdict


class DaySix(DayType):
    day_name: str = "day06"

    def parse_data(self, data: list[str]):
        col_dict = defaultdict(list)
        col_ops = defaultdict(str)

        for index, row in enumerate(data):
            split_row = row.split()
            if index == len(data) - 1:
                for op_index, op in enumerate(split_row):
                    col_ops[op_index] = op
            else:
                for col_index, val in enumerate(split_row):
                    col_dict[col_index].append(int(val))

        return col_dict, col_ops

    def parse_data_p2(self, data: list[str]):
        return data

    def part_one(self, data: List[str]):
        total_sum = 0
        col_dict, col_ops = self.parse_data(data)
        for idx, int_arr in col_dict.items():
            opp = col_ops[idx]
            match opp:
                case "+":
                    total_sum += sum(int_arr)
                case "*":
                    product = 1
                    for val in int_arr:
                        product *= val
                    total_sum += product
        return total_sum

    def part_two(self, data: List[str]):
        return 0
