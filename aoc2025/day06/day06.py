from traceback import print_list
from data_loader import DayType
from typing import List
from collections import defaultdict, deque


class DaySix(DayType):
    day_name: str = "day06"

    def parse_data_p1(self, data: list[str]):
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
        last_line = data[-1]
        rem = data[:-1]
        delims = [idx for idx, char in enumerate(last_line) if char in "*+"]
        ops = [char for char in last_line if char in "*+"]

        columns = [
            [list(line[start:delims[idx + 1] - 1].replace(" ", "0")) for idx, start in enumerate(delims[: - 1])]
            for line in rem
        ]

        chunked = list(zip(*columns))
        
        last_line = []
        for line in rem:
            last_line.append(list(line[delims[-1]: ].replace(" ", "0")))
        
        chunked.append(last_line)
        return zip(chunked, ops)
       
    def part_one(self, data: List[str]):
        total_sum = 0
        col_dict, col_ops = self.parse_data_p1(data)
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
        col_ops = self.parse_data_p2(data)
        total = 0
        for cols, op in col_ops:
            this_row = defaultdict(list)
            for col in cols:
                for idx in range(len(col) - 1, -1, -1):
                    value = col[idx]
                    if value == "0":
                        continue
                    this_row[idx].append(value)
            rows = [int("".join(l)) for l in this_row.values()]
            match op:
                case "+":
                    total += sum(rows)
                case "*":
                    product = 1
                    for val in rows:
                        product *= val
                    total += product
        return total