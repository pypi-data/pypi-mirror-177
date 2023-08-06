from typing import Optional, NoReturn, List, Any, Dict, Union

import numpy as np

from decision_tree.metrics import gini, entropy, gain
from decision_tree.node import DecisionTreeLeaf, DecisionTreeNode


class DecisionTreeClassifier:
    """
    Attributes
    ----------
    root : Union[DecisionTreeNode, DecisionTreeLeaf]
        Корень дерева.

    (можете добавлять в класс другие аттрибуты).

    """

    def __init__(self, criterion: str = "gini",
                 max_depth: Optional[int] = None,
                 min_samples_leaf: int = 1):
        """
        Parameters
        ----------
        criterion : str
            Задает критерий, который будет использоваться при построении дерева.
            Возможные значения: "gini", "entropy".
        max_depth : Optional[int]
            Ограничение глубины дерева. Если None - глубина не ограничена.
        min_samples_leaf : int
            Минимальное количество элементов в каждом листе дерева.

        """
        self.root = None
        self.criterion = gini if criterion == "gini" else entropy
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf

    def fit(self, X: np.ndarray, y: np.ndarray) -> NoReturn:
        """
        Строит дерево решений по обучающей выборке.

        Parameters
        ----------
        X : np.ndarray
            Обучающая выборка.
        y : np.ndarray
            Вектор меток классов.
        """
        self.root = self._build(X, y, 0)

    def predict_proba(self, X: np.ndarray) -> List[Dict[Any, float]]:
        """
        Предсказывает вероятность классов для элементов из X.

        Parameters
        ----------
        X : np.ndarray
            Элементы для предсказания.

        Return
        ------
        List[Dict[Any, float]]
            Для каждого элемента из X возвращает словарь
            {метка класса -> вероятность класса}.
        """
        ans = []
        for x in X:
            cur = self.root
            while not isinstance(cur, DecisionTreeLeaf):
                if x[cur.split_dim] < cur.split_value:
                    cur = cur.left
                else:
                    cur = cur.right
            ans.append(cur.m)
        return ans

    def predict(self, X: np.ndarray) -> list:
        """
        Предсказывает классы для элементов X.

        Parameters
        ----------
        X : np.ndarray
            Элементы для предсказания.

        Return
        ------
        list
            Вектор предсказанных меток для элементов X.
        """
        proba = self.predict_proba(X)
        return [max(p.keys(), key=lambda k: p[k]) for p in proba]

    def _build(self, X: np.ndarray, y: np.ndarray, depth: int) -> Union['DecisionTreeNode', DecisionTreeLeaf]:
        if len(np.unique(y)) == 1:
            return DecisionTreeLeaf(y)

        if depth == self.max_depth:
            return DecisionTreeLeaf(y)

        if len(y) < 2 * self.min_samples_leaf:
            return DecisionTreeLeaf(y)

        dim = -1
        threshold = -1
        inf_gain = 0

        for i in range(X.shape[1]):
            ind = list(range(X.shape[0]))
            ind.sort(key=lambda k: X[k][i])
            for j in range(self.min_samples_leaf, X.shape[0] - self.min_samples_leaf):
                cur_gain = gain(y[ind[:j]], y[ind[j:]], self.criterion)
                if cur_gain > inf_gain:
                    dim = i
                    threshold = X[ind[j]][i]
                    inf_gain = cur_gain

        if dim == -1:
            return DecisionTreeLeaf(y)

        left = [i for i, (x, _) in enumerate(zip(X, y)) if x[dim] < threshold]
        right = [i for i, (x, _) in enumerate(zip(X, y)) if x[dim] >= threshold]

        return DecisionTreeNode(dim, threshold,
                                self._build(X[left], y[left], depth + 1),
                                self._build(X[right], y[right], depth + 1)
                                )
