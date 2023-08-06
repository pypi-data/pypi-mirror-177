import os.path

from sklearn.datasets import make_moons

from decision_tree.classifier import DecisionTreeClassifier
from decision_tree.draw_tree import draw_tree
from decision_tree.plots import plot_2d, plot_roc_curve


def main():
    noise = 0.35
    X, y = make_moons(1500, noise=noise)
    X_test, y_test = make_moons(200, noise=noise)
    tree = DecisionTreeClassifier(max_depth=5, min_samples_leaf=30)
    tree.fit(X, y)
    if not os.path.exists('../plots'):
        os.mkdir('../plots')
    plot_2d(tree, X, y, save_path='../plots/2d.png')
    plot_roc_curve(y_test, tree.predict_proba(X_test), save_path='../plots/roc_curve.png')
    draw_tree(tree, save_path='../plots/tree.png')


if __name__ == "__main__":
    main()
