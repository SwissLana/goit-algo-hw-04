# Порівняння алгоритмів сортування: Merge Sort, Insertion Sort, Timsort 
import random # для генерації випадкових чисел 
import timeit # для вимірювання часу 
from statistics import mean # для усереднення результатів timeit 
from typing import Callable, Dict, List, Tuple, Optional # для типізації 


def insertion_sort(arr: List[int]) -> List[int]:
    a = arr[:] # робимо копію, щоб не змінювати вхідний масив 
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1: # базовий випадок 
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]: # зливає два відсортовані масиви 
    i = j = 0
    out: List[int] = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    if i < len(left): out.extend(left[i:])
    if j < len(right): out.extend(right[j:])
    return out

def timsort(arr: List[int]) -> List[int]: 
    return sorted(arr)


def gen_random(n: int) -> List[int]: # генерує випадковий масив з n елементів 
    return [random.randint(-10**6, 10**6) for _ in range(n)]

def gen_sorted(n: int) -> List[int]: # генерує відсортований масив з n елементів 
    return list(range(n))

def gen_reverse(n: int) -> List[int]: # генерує відсортований у зворотньому порядку масив з n елементів 
    return list(range(n, 0, -1))

def gen_nearly_sorted(n: int) -> List[int]: # генерує майже відсортований масив з n елементів 
    a = list(range(n))
    swaps = max(1, n // 200)  # кілька дрібних перестановок
    for _ in range(swaps):
        i = random.randrange(n); j = random.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a


Algo = Callable[[List[int]], List[int]] # тип для алгоритму сортування 

ALGORITHMS: Dict[str, Algo] = {
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Timsort (sorted)": timsort,
}

GENERATORS: Dict[str, Callable[[int], List[int]]] = {
    "random": gen_random,
    "sorted": gen_sorted,
    "reverse": gen_reverse,
    "nearly_sorted": gen_nearly_sorted,
}

SIZES = [500, 2000, 6000, 12000]   # розміри масивів
REPEATS = 3                        # повтори timeit для усереднення
INSERTION_MAX_N = 6000             # щоб не чекати дуже довго на O(n^2)

# Вимірює середній час виконання алгоритму сортування на масиві arr 
def time_algo(algo: Algo, arr: List[int], repeats: int = REPEATS) -> float:
    t = timeit.Timer(lambda: algo(arr)).repeat(repeat=repeats, number=1)
    return mean(t)

# Запускає бенчмарк для всіх алгоритмів і наборів даних 
def run_benchmark() -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for dist_name, gen in GENERATORS.items():
        for n in SIZES:
            base = gen(n) # генеруємо вхідний масив 
            
            # готуємо рядок для терміналу
            row_out = f"[n={n:<6} | {dist_name:<12}]"

            times_for_line = {} # збираємо часи для виводу в один рядок терміналу 
            
            for algo_name, algo in ALGORITHMS.items():
                # пропускаємо insertion_sort на надто великому n
                if algo_name == "Insertion Sort" and n > INSERTION_MAX_N:
                    avg = None
                else:
                    avg = time_algo(algo, base)

                results.append({
                    "dataset": dist_name, "n": n,
                    "algorithm": algo_name, "time": avg
                })
                times_for_line[algo_name] = avg

            # вивід у термінал у потрібному форматі
            row_out += f" insertion: {fmt_time(times_for_line['Insertion Sort'])}s"
            row_out += f"  merge: {fmt_time(times_for_line['Merge Sort'])}s"
            row_out += f"  timsort: {fmt_time(times_for_line['Timsort (sorted)'])}s"
            print(row_out)
            
    return results

# Форматує час для виводу (або "—", якщо None) 
def fmt_time(t: Optional[float]) -> str:
    return f"{t:.6f}" if t is not None else "—"

# Вивід результатів у термінал у вигляді зведеної таблиці 
def print_terminal_summary(results: List[Dict[str, object]]):
    # згрупуємо за розміром n 
    by_n: Dict[int, List[Dict[str, object]]] = {}
    for r in results:
        by_n.setdefault(r["n"], []).append(r)
    # вивід по n 
    for n in sorted(by_n.keys()):
        print(f"\n=== n = {n} ===")
        rows = by_n[n]
        # групуємо по dataset
        by_dataset: Dict[str, Dict[str, Optional[float]]] = {}
        for r in rows:
            by_dataset.setdefault(r["dataset"], {})[r["algorithm"]] = r["time"]
        for dataset, algos in by_dataset.items():
            line = f"{dataset:<13}→"
            line += f" insertion: {fmt_time(algos.get('Insertion Sort'))}s"
            line += f"  merge: {fmt_time(algos.get('Merge Sort'))}s"
            line += f"  timsort: {fmt_time(algos.get('Timsort (sorted)'))}s"
            print(line)

def build_markdown(results: List[Dict[str, object]]) -> str:
    # згрупуємо за набором і розміром
    by_set: Dict[Tuple[str, int], List[Dict[str, object]]] = {}
    for r in results:
        key = (r["dataset"], r["n"])
        by_set.setdefault(key, []).append(r)

    lines: List[str] = []
    lines.append("# Порівняння алгоритмів сортування: Merge Sort, Insertion Sort, Timsort\n")
    lines.append(f"Набори даних: `random`, `sorted`, `reverse`, `nearly_sorted`.\n"
                 f"Розміри: {SIZES}. Повторів: {REPEATS}.\n"
                 f"Для **Insertion Sort** великі `n` (> {INSERTION_MAX_N}) пропущено, щоб уникнути надто довгого очікування.\n")

    # Зведена таблиця (рядки — набори, колонки — алгоритми) 
    order_sets = list(GENERATORS.keys())
    lines.append("## Результати порівнянь алгоритмів сортування\n")
    by_n: Dict[int, List[Dict[str, object]]] = {}
    for r in results:
        by_n.setdefault(r["n"], []).append(r)
    for n in sorted(by_n.keys()):
        lines.append(f"\n### n = {n}\n")
        lines.append("| Dataset | Insertion Sort | Merge Sort | Timsort |")
        # зберігаємо порядок наборів
        rows = by_n[n]
        by_dataset: Dict[str, Dict[str, Optional[float]]] = {}
        for r in rows:
            by_dataset.setdefault(r["dataset"], {})[r["algorithm"]] = r["time"]
        for dataset in order_sets:
            algos = by_dataset.get(dataset, {})
            lines.append(f"| {dataset:<12} | {fmt_time(algos.get('Insertion Sort'))} | "
                         f"{fmt_time(algos.get('Merge Sort'))} | "
                         f"{fmt_time(algos.get('Timsort (sorted)'))} |")
        
    lines.append("\n")
    
    # Детальніше по наборах 
    lines.append("\n## Детальніше по наборах\n")
    for dataset in order_sets:
        lines.append(f"\n## Набір даних: **{dataset}**\n")
        for n in SIZES:
            rows = by_set.get((dataset, n), [])
            if not rows:
                continue
            # визначимо найшвидший (ігноруємо None)
            best_algo, best_time = None, None
            for r in rows:
                t = r["time"]
                if t is None: 
                    continue
                if best_time is None or t < best_time:
                    best_time = t
                    best_algo = r["algorithm"]

            lines.append(f"### n = {n}\n")
            lines.append("| Алгоритм | Середній час (с) |")
            # стабільний порядок виводу
            for algo_name in ["Insertion Sort", "Merge Sort", "Timsort (sorted)"]:
                t = next((r["time"] for r in rows if r["algorithm"] == algo_name), None)
                lines.append(f"| {algo_name} | {fmt_time(t)} |")
            if best_algo is not None:
                lines.append(f"\n**Найшвидший:** {best_algo} — {best_time:.6f} с.\n")
            else:
                lines.append("\n**Найшвидший:** (недоступно — усі значення пропущені)\n")
        
    return "\n".join(lines)

def main():
    results = run_benchmark()
    print_terminal_summary(results)
    md = build_markdown(results)
    out = "task3_results.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\nГотово! Звіт збережено у {out}")

if __name__ == "__main__":
    main()