from typing import List, Tuple, Generator
import math
from data_loader import DayType
from dataclasses import dataclass


class DayTwo(DayType):
    day_name: str = "day02"

    def parse_input(self, rows: List[str]) -> Generator[Tuple[int, int]]:
        for row in rows:
            row = row.split(",")
            for idx in range(len(row)):
                to_parse = tuple(int(i) for i in row[idx].split("-"))
                yield to_parse

    def number_is_contained(self, num: int) -> bool:
        num_digits = int(math.log10(num)) + 1
        half = num_digits // 2
        divisor = 10**half
        left = num // divisor
        right = num % divisor
        return left == right

    def part_one(self, data: List[Tuple[int, int]]):
        total_count = 0

        for t in self.parse_input(data):
            start, end = t
            # given_range = end - start
            range_object = range(start, end + 1)

            for given_num in range_object:
                if self.number_is_contained(given_num):
                    total_count += given_num

        return total_count

    def detect_chunks(self, chunk_amount: int, given_str: str) -> bool:
        if len(given_str) % chunk_amount != 0:
            return False

        left = given_str[:chunk_amount]
        for idx in range(chunk_amount, len(given_str), chunk_amount):
            if given_str[idx : idx + chunk_amount] != left:
                return False

        return True

    def count_window(self, num: int) -> int:
        counts = set()
        as_str = str(num)
        half = len(as_str) // 2
        chunk = 1

        while chunk <= half:
            if len(as_str) % chunk != 0:
                chunk += 1
                continue
            if self.detect_chunks(chunk, as_str):
                counts.add(num)
            chunk += 1
        return sum(counts)

    def part_two(self, data: List[str]) -> int:
        total_count = 0

        for t in self.parse_input(data):
            start, end = t
            # given_range = end - start
            range_object = range(start, end + 1)
            for num in range_object:
                total_count += self.count_window(num)

        return total_count
