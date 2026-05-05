from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)


@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]


@dataclass(frozen=True)
class Node:
    value: Row
    next: Optional[Node]


EXPECTED_HEADER = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]


def float_or_none(value: str) -> Optional[float]:
    value = value.strip()
    if value == "" or value == "''" or value == '""':
        return None
    return float(value)


def parse_row(fields: list[str]) -> Row:
    return Row(
        country=fields[0],
        year=int(fields[1]),
        electricity_and_heat_co2_emissions=float_or_none(fields[2]),
        electricity_and_heat_co2_emissions_per_capita=float_or_none(fields[3]),
        energy_co2_emissions=float_or_none(fields[4]),
        energy_co2_emissions_per_capita=float_or_none(fields[5]),
        total_co2_emissions_excluding_lucf=float_or_none(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita=float_or_none(fields[7]),
    )


def build_linked_list(rows: list[list[str]], index: int) -> Optional[Node]:
    if index >= len(rows):
        return None
    return Node(parse_row(rows[index]), build_linked_list(rows, index + 1))


def read_csv_lines(filename: str) -> Optional[Node]:
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        if header != EXPECTED_HEADER:
            raise ValueError(f"Expected header {EXPECTED_HEADER}, got {header}")

        rows = list(reader)

    return build_linked_list(rows, 0)


def listlen(data: Optional[Node]) -> int:
    if data is None:
        return 0
    return 1 + listlen(data.next)


def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:
    if data is None:
        return None

    row = data.value
    field_val = getattr(row, field_name)

    if field_val is None:
        return filter_rows(data.next, field_name, comparison, value)

    if field_name == "country" and comparison != "equal":
        raise ValueError("country only supports equal")

    if comparison == "equal":
        match = field_val == value
    elif comparison == "less_than":
        match = field_val < value
    elif comparison == "greater_than":
        match = field_val > value
    else:
        raise ValueError("invalid comparison")

    filtered_rest = filter_rows(data.next, field_name, comparison, value)

    if match:
        return Node(row, filtered_rest)
    return filtered_rest