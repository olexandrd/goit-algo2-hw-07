import timeit
from functools import lru_cache
from splay_tree import SplayTree


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
    return fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)


def measure_time(func, *args):
    execution_time = timeit.timeit(lambda: func(*args), number=5)
    return execution_time


def main():
    fibonacci_seed_list = [x * 5 for x in range(20)]
    for seed in fibonacci_seed_list:
        splay_tree = SplayTree()
        print(f"Seed: {seed}")
        print(f"LRU: {measure_time(fibonacci_lru, (seed))}")
        splay_tree = SplayTree()
        print(f"Splay: {measure_time(fibonacci_splay, seed, splay_tree)}")


if __name__ == "__main__":
    main()
