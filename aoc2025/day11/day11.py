from functools import cache
from typing import Dict, FrozenSet, List, Tuple

from data_loader import DayType


def parse_graph(data: List[str]) -> Dict[str, Tuple[str, ...]]:
    graph = {}
    for line in data:
        node, neighbors = line.split(":")
        graph[node] = tuple(neighbors.split())
    return graph


def count_paths(graph: Dict[str, Tuple[str, ...]]) -> int:
    @cache
    def dfs(node: str) -> int:
        if node == "out":
            return 1
        return sum(dfs(neighbor) for neighbor in graph[node])

    return dfs("you")


def count_paths_through_nodes(
    graph: Dict[str, Tuple[str, ...]], required_nodes: FrozenSet[str]
) -> int:
    @cache
    def dfs(node: str, seen: FrozenSet[str]) -> int:
        if node == "out":
            return 1 if required_nodes <= seen else 0
        new_seen = seen | ({node} & required_nodes)
        return sum(dfs(neighbor, new_seen) for neighbor in graph[node])

    return dfs("svr", frozenset())


class DayEleven(DayType):
    day_name: str = "day11"

    def part_one(self, data: List[str]) -> int:
        graph = parse_graph(data)
        return count_paths(graph)

    def part_two(self, data: List[str]) -> int:
        graph = parse_graph(data)
        return count_paths_through_nodes(graph, frozenset({"dac", "fft"}))
