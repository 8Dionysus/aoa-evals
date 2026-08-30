"""Synthetic symbols used only for local provider-observation evidence."""

from math import sqrt


def rename_symbol(value: int) -> int:
    return value


def move_symbol(value: int) -> int:
    return value + 1


def signature_change(value: int, offset: int = 0) -> int:
    return value + offset


class AddedEntity:
    """A class added to the synthetic source graph."""

    pass


def delete_entity(value: int) -> int:
    return value - 1


def import_change(value: int) -> float:
    return sqrt(value)


def multi_file_impact(value: int) -> int:
    return rename_symbol(value) + move_symbol(value)


def split_left(value: int) -> int:
    return value // 2


def split_right(value: int) -> int:
    return value - split_left(value)


def merge_left(value: int) -> int:
    return value + 2


def merge_right(value: int) -> int:
    return value + 3


def stale_index(value: int) -> int:
    return value


def delta_full_parity(value: int) -> int:
    return value * 2


def affected_test_selection(value: int) -> int:
    return value % 2
