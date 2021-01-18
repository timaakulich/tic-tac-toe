import numpy as np

from app.game import get_winners


def test_game_winners():
    matrix = np.array([
        ["x", "-", "o"],
        ["x", "o", "-"],
        ["x", "-", "o"],
    ])
    assert set(get_winners(matrix, 3)) == {"x"}

    matrix = np.array([
        ["x", "-", "o"],
        ["o", "o", "x"],
        ["x", "-", "o"],
    ])
    assert set(get_winners(matrix, 3)) == set()

    matrix = np.array([
        ["x", "-", "o"],
        ["o", "x", "x"],
        ["x", "o", "x"],
    ])
    assert set(get_winners(matrix, 3)) == {"x"}

    matrix = np.array([
        ["x", "-", "o"],
        ["x", "-", "o"],
        ["x", "-", "o"],
    ])
    assert set(get_winners(matrix, 3)) == {"o", "x"}
