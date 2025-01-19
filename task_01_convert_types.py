import random
import time
from functools import lru_cache

cache_size = 1000


def generate_array(n):
    return [random.randint(1, n) for i in range(n)]


def generate_request(n, q):
    return [
        (
            random.choices(["Range", "Update"], weights=[0.9, 0.1])[0],
            random.randint(0, n - 1),
            random.randint(0, n - 1),
        )
        for i in range(q)
    ]


def range_sum_no_cache(array, L, R):
    if L > R:
        L, R = R, L
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


@lru_cache(maxsize=cache_size)
def range_sum_with_cache(string, L, R):
    arr = list(map(int, string.replace("[", "").replace("]", "").split(", ")))
    if L > R:
        L, R = R, L
    return sum(arr[L : R + 1])


def update_with_cache(arr, index, value):
    arr[index] = value

    range_sum_with_cache.cache_clear()


def main():
    conditions = [
        {
            "n": 100,
            "q": 50000,
        },
        {
            "n": 1000,
            "q": 500000,
        },
        {"n": 100, "q": 5000000},
        {
            "n": 10000,
            "q": 5000000,
        },
        {
            "n": 100000,
            "q": 50000,
        },
    ]
    for condition in conditions:
        n = condition["n"]
        q = condition["q"]
        print(f"n = {n}, q = {q}")
        arr = generate_array(n)
        request = generate_request(n, q)
        cache_hits = []
        start0 = time.time()
        for r in request:
            if r[0] == "Range":
                range_sum_no_cache(arr, r[1], r[2])
            elif r[0] == "Update":
                update_no_cache(arr, r[1], r[2])
        print(f"Час виконання без кешування: {round(time.time() - start0, 2)} секунд")
        start1 = time.time()
        for r in request:
            if r[0] == "Range":
                range_sum_with_cache(str(arr), r[1], r[2])
                cache_hits.append(range_sum_with_cache.cache_info().hits)
            elif r[0] == "Update":
                update_with_cache(arr, r[1], r[2])
        cache_exec_time = time.time() - start1
        total_cache_hits = sum(
            cache_hits[i]
            for i in range(len(cache_hits) - 1)
            if cache_hits[i] > cache_hits[i + 1]
        )
        print(
            f"Час виконання з LRU-кешем: {round(cache_exec_time, 2)} секунд, загальна кількість попадань в кеш: {total_cache_hits}"
        )


if __name__ == "__main__":
    main()
