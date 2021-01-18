import re
from enum import Enum
from typing import Union

import numpy as np


class Mark(str, Enum):
    X_MARK = "x"
    O_MARK = "o"
    EMPTY_MARK = "-"

    @classmethod
    def get_opposite_mark(cls, mark: "Mark") -> Union["Mark", None]:
        return {
            cls.X_MARK: cls.O_MARK,
            cls.O_MARK: cls.X_MARK
        }.get(mark)


def _get_matrix_rows_columns_diagonals(matrix: np.ndarray):
    yield from iter(matrix)
    yield from iter(matrix.transpose())
    yield from (
        matrix[::-1, :].diagonal(i)
        for i in range(-matrix.shape[0] + 1, matrix.shape[1])
    )
    yield from (
        matrix.diagonal(i)
        for i in range(matrix.shape[1] - 1, -matrix.shape[0], -1)
    )


def get_winners(matrix: np.ndarray, win_length: int) -> Union[Mark, None]:
    patterns = {
        Mark.X_MARK: re.compile(f"{Mark.X_MARK.value}{{{win_length}}}"),
        Mark.O_MARK: re.compile(f"{Mark.O_MARK.value}{{{win_length}}}")
    }
    for row in _get_matrix_rows_columns_diagonals(np.array(matrix)):
        row_str = "".join(map(str, row))
        for mark, pattern in patterns.items():
            if pattern.match(row_str):
                yield mark
