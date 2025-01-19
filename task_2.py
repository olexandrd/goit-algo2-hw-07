from collections import defaultdict
import sys
import timeit
from functools import lru_cache
from splay_tree import SplayTree
from matplotlib import pyplot as plt

sys.setrecursionlimit(9000)


@lru_cache(maxsize=1000)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n < 2:
        return n
    if tree.find(n) is None:
        tree.insert(n)
    else:
        return tree.find(n)
    return fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)


def measure_time(func, *args):
    execution_time = timeit.timeit(lambda: func(*args), number=5)
    return execution_time


def plot_results(results):
    x = [x for x in results.keys()]
    y_lru = [results[seed]["lru"] for seed in results.keys()]
    y_splay = [results[seed]["splay"] for seed in results.keys()]

    plt.plot(x, y_lru, label="LRU")
    plt.plot(x, y_splay, label="Splay")
    plt.xlabel("N")
    plt.ylabel("Execution time (s)")
    plt.title("Execution time of Fibonacci sequence calculation")
    plt.legend()
    plt.show()


def main():
    fibonacci_seed_list = [x * 50 for x in range(20)]
    results = defaultdict(dict)
    for seed in fibonacci_seed_list:
        splay_tree = SplayTree()
        results[seed]["lru"] = measure_time(fibonacci_lru, seed)
        results[seed]["splay"] = measure_time(fibonacci_splay, seed, splay_tree)

    print("Seed\t\tLRU time (s)\tSplay time (s)")
    row_format = "{:<15} {:<15} {:<15}"
    print("-" * 45)
    for seed, values in results.items():
        print(
            row_format.format(
                seed, round(values["lru"], 10), round(values["splay"], 10)
            )
        )
    plot_results(results)


if __name__ == "__main__":
    main()
