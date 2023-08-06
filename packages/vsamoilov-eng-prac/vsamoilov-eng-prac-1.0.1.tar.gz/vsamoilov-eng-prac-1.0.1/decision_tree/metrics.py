from collections import defaultdict
from typing import Callable

import numpy as np


def gini(x: np.ndarray) -> float:
    """
    Считает коэффициент Джини для массива меток x.
    """
    m = defaultdict(int)
    for y in x:
        m[y] += 1
    m = np.array(list(m.values())) / x.shape[0]
    res = m.dot(1 - m)
    # print("Giny=", res)
    return res


def entropy(x: np.ndarray) -> float:
    """
    Считает энтропию для массива меток x.
    """
    m = defaultdict(int)
    for y in x:
        m[y] += 1
    m = np.array(list(m.values())) / x.shape[0]
    res = -np.sum(m * np.log2(m))
    # print("Entropy=", res)
    return res


def gain(left_y: np.ndarray, right_y: np.ndarray, criterion: Callable) -> float:
    """
    Считает информативность разбиения массива меток.

    Parameters
    ----------
    left_y : np.ndarray
        Левая часть разбиения.
    right_y : np.ndarray
        Правая часть разбиения.
    criterion : Callable
        Критерий разбиения.
    """
    res = criterion(np.concatenate([left_y, right_y])) * (len(left_y) + len(right_y)) - len(right_y) * criterion(
        right_y) - len(left_y) * criterion(left_y)
    return res