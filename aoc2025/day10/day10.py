from typing import List
from z3 import z3
from data_loader import DayType


def parse_bracketed(text: str) -> str:
    return text[1:-1]


def parse_int_list(text: str) -> List[int]:
    return [int(x) for x in parse_bracketed(text).split(",")]


def pattern_to_bitmask(pattern: str) -> int:
    return sum(1 << i for i, c in enumerate(pattern) if c == "#")


def positions_to_bitmask(positions: List[int]) -> int:
    return sum(1 << pos for pos in positions)


class DayTen(DayType):
    day_name: str = "day10"

    def part_one(self, data: List[str]):
        total = 0
        for line in data:
            words = line.split()
            goal_mask = pattern_to_bitmask(parse_bracketed(words[0]))

            button_positions = [parse_int_list(b) for b in words[1:-1]]
            button_masks = [positions_to_bitmask(pos) for pos in button_positions]

            num_buttons = len(button_masks)
            min_presses = num_buttons

            for combo in range(1 << num_buttons):
                result_mask = 0
                press_count = 0
                for i, mask in enumerate(button_masks):
                    if combo & (1 << i):
                        result_mask ^= mask
                        press_count += 1
                if result_mask == goal_mask:
                    min_presses = min(min_presses, press_count)

            total += min_presses
        return total

    def part_two(self, data: List[str]):
        total = 0
        for line in data:
            words = line.split()
            button_positions = [parse_int_list(b) for b in words[1:-1]]
            target_values = parse_int_list(words[-1])
            button_vars = [z3.Int(f"button_{i}") for i in range(len(button_positions))]
            optimizer = z3.Optimize()
            for var in button_vars:
                optimizer.add(var >= 0)
            for pos_idx, target in enumerate(target_values):
                affecting_buttons = [
                    button_vars[btn_idx]
                    for btn_idx, positions in enumerate(button_positions)
                    if pos_idx in positions
                ]
                if affecting_buttons:
                    optimizer.add(sum(affecting_buttons) == target)

            optimizer.minimize(sum(button_vars))
            assert optimizer.check() == z3.sat
            model = optimizer.model()
            total += sum(model[var].as_long() for var in button_vars)

        return total
