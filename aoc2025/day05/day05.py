from data_loader import DayType
from typing import List


class DayFive(DayType):
    day_name = "day05"

    def compress_interval(self, intervals: List[int, int]):
        intervals.sort()
        processed_intervals = [intervals[0]]

        for interval in intervals[1:]:
            last_interval = processed_intervals[-1]
            if last_interval[1] >= interval[0]:
                new_range = (
                    last_interval[0],
                    max(last_interval[1], interval[1]),
                )
                processed_intervals[-1] = new_range
            else:
                processed_intervals.append(interval)

        return processed_intervals

    def parse_data(self, data: List[str]):
        intervals = []
        food_ids = []

        on_intervals = True
        for line in data:
            if line == "":
                on_intervals = False
            elif on_intervals:
                l, r = [*map(int, line.split("-"))]
                intervals.append((l, r))
            else:
                food_ids.append(int(line))

        return self.compress_interval(intervals), food_ids

    def part_one(self, data: List[str]):
        intervals, food_ids = self.parse_data(data)
        count = 0

        for food_id in food_ids:
            count += any(
                (
                    food_id >= interval[0] and food_id <= interval[1]
                    for interval in intervals
                )
            )

        return count

    def part_two(self, data):
        intervals, _ = self.parse_data(data)
        total_ids = 0
        for left, right in intervals:
            total_ids += (right - left + 1)
        return total_ids
