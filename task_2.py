from collections import defaultdict
import sys
import timeit
from functools import lru_cache
from splay_tree import SplayTree

sys.setrecursionlimit(3000)


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


if __name__ == "__main__":
    main()
