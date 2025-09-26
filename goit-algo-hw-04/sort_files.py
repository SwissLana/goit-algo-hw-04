import argparse # для парсингу аргументів командного рядка
import shutil # для копіювання файлів
import sys  # для виводу помилок та попереджень
import shlex # для коректного розбиття рядка з шляхами
from pathlib import Path # для роботи з файловими шляхами
from collections import defaultdict # для підрахунку статистики за розширеннями

# ANSI кольори для виводу
COLOR_BLUE = "\033[94m"   # для тек у дереві та чисел у підсумку
COLOR_GREEN = "\033[92m"  # для позначки "Готово" та загального підсумку 
COLOR_RESET = "\033[0m"   # скидання кольору до стандартного 

# Відображає структуру теки у вигляді дерева
def display_tree(path: Path, indent: str = "", prefix: str = "") -> None:
    if path.is_dir():
        # відображає теки синім кольором
        print(indent + prefix + COLOR_BLUE + path.name + COLOR_RESET)
        indent += "    " if prefix else ""
        # сортуємо: спочатку теки, потім файли, обидва за алфавітом без урахування регістру
        children = [c for c in path.iterdir() if not c.name.startswith(".DS_Store")]
        children = sorted(children, key=lambda x: (x.is_file(), x.name.lower()))
        for index, child in enumerate(children):
            is_last = index == len(children) - 1
            display_tree(child, indent, "└── " if is_last else "├── ")
    else:
        if not path.name.startswith(".DS_Store"):
            print(indent + prefix + path.name)

# Парсить аргументи командного рядка 
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли зі source в dest і сортує їх за розширеннями."
    )
    parser.add_argument("source", type=Path, nargs="?", help="Шлях до вихідної директорії")
    parser.add_argument(
        "dest", type=Path, nargs="?", default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: ./dist)"
    )
    return parser.parse_args()

# Перевіряє, чи знаходиться child всередині parent у файловій системі 
def is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False

# Копіює файл у теку за розширенням у dest_root 
def copy_file_to_ext_dir(file_path: Path, dest_root: Path) -> None:
    if file_path.name.startswith(".DS_Store"):
        return False
    # визначаємо розширення (без крапки, у нижньому регістрі); якщо немає — "no_ext" 
    ext = file_path.suffix.lower().lstrip(".") or "no_ext"
    target_dir = dest_root / ext
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Немає прав для створення теки: {target_dir} — {e}", file=sys.stderr)
        return
    except OSError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Помилка створення теки: {target_dir} — {e}", file=sys.stderr)
        return

    target_path = target_dir / file_path.name # цільовий шлях копіювання
    
    if target_path.exists():
        return False  # пропускаємо, якщо файл уже існує
    
    try:
        shutil.copy2(file_path, target_path)
        
    except PermissionError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Немає прав для копіювання: {file_path} — {e}", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Файл не знайдено під час копіювання: {file_path} — {e}", file=sys.stderr)
    except OSError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Помилка копіювання {file_path} -> {target_path} — {e}", file=sys.stderr)

# Рекурсивно обходить source і копіює файли у dest_root 
def walk_and_copy(source: Path, dest_root: Path) -> None:
    try:
        entries = list(source.iterdir())
    except PermissionError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Немає прав для читання: {source} — {e}", file=sys.stderr)
        return
    except FileNotFoundError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Теку не знайдено: {source} — {e}", file=sys.stderr)
        return
    except OSError as e:
        print(f"[ПОПЕРЕДЖЕННЯ] Помилка читання теки {source} — {e}", file=sys.stderr)
        return

    for entry in entries: # ітеруємося по вмісту теки source 
        if entry.is_dir():
            # пропускаємо гілку, якщо dest лежить у цій підтеці
            if is_within(dest_root, entry):
                continue
            walk_and_copy(entry, dest_root)
        elif entry.is_file():
            if entry.name.startswith(".DS_Store"):
                continue
            copy_file_to_ext_dir(entry, dest_root)
            
# Збирає статистику по кількості файлів за розширеннями у dest
def collect_stats(dest: Path) -> dict[str, int]:
    stats: dict[str, int] = defaultdict(int)
    if not dest.exists():
        return stats
    for ext_dir in dest.iterdir():
        if ext_dir.is_dir():
            ext = ext_dir.name
            files = [f for f in ext_dir.iterdir() if f.is_file() and not f.name.startswith(".DS_Store")]
            stats[ext] += len(files)
    return stats

# Виводить підсумкову статистику за розширеннями 
def print_summary(stats: dict[str, int]) -> None:
    total = sum(stats.values())
    print(f"\n   {COLOR_GREEN}Результат сортування:{COLOR_RESET}\n")
    if not stats:
        print("  У директорії немає файлів.")
    else:
        for ext, count in sorted(stats.items()):
            print(f"  {ext:<10} {COLOR_BLUE}{count:>5}{COLOR_RESET} файл(и)")
        print("  " + "-"*24)
        print(f"  {COLOR_GREEN}TOTAL{COLOR_RESET}       {COLOR_BLUE}{total:>5}{COLOR_RESET} {COLOR_GREEN}файл(и){COLOR_RESET}")
    

def main() -> int:
    args = parse_args()

    # якщо source не передали як аргумент — запитуємо шляхи одним рядком
    if args.source is None:
        line = input(
            "Введіть шлях до вихідної та директорії призначення "
            "(якщо вказана тільки вихідна директорія — файли будуть автоматично збережені у 'dist'):\n> "
        ).strip()

        parts = shlex.split(line)  # коректно розбиває з урахуванням лапок/пробілів у шляхах
        if not parts:
            print("[ПОМИЛКА] Не вказано шлях до вихідної директорії.", file=sys.stderr)
            return 2

        src = Path(parts[0]).expanduser()  # перший аргумент — source
        dst = Path(parts[1]).expanduser() if len(parts) > 1 else Path("dist") # другий — dest або 'dist' за замовчуванням
    else:
        # якщо source передали — беремо його
        src = args.source
        # якщо dest передали — беремо його; якщо ні — 'dist' за замовчуванням
        dst = args.dest or Path("dist")
    
    # перевірки валідності шляхів 
    if not src.exists():
        print(f"[ПОМИЛКА] Вихідна директорія не існує: {src}", file=sys.stderr)
        return 2
    if not src.is_dir():
        print(f"[ПОМИЛКА] Шлях не є директорією: {src}", file=sys.stderr)
        return 2

    try:
        dst.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"[ПОМИЛКА] Немає прав для створення теки призначення: {dst} — {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"[ПОМИЛКА] Неможливо створити теку призначення {dst} — {e}", file=sys.stderr)
        return 2

    # якщо dest всередині source — попереджаємо
    if is_within(dst, src):
        print(f"[ПОПЕРЕДЖЕННЯ] Тека призначення {dst} знаходиться всередині вихідної {src}.", file=sys.stderr)
        print("  Файли в теці призначення будуть пропущені під час копіювання.", file=sys.stderr)

    walk_and_copy(src, dst)
    # показуємо дерево каталогу призначення для візуальної перевірки
    print(f"\n{COLOR_GREEN}[Готово]{COLOR_RESET} Файли з '{src}' скопійовані в '{dst}' і відсортовані за розширенням.")
    print(f"\n📂 {COLOR_GREEN}Структура теки призначення:{COLOR_RESET}\n")
    display_tree(dst)
    
    # підсумковий звіт про кількість файлів за розширеннями 
    final_stats = collect_stats(dst)
    print_summary(final_stats)
    return 0
    

if __name__ == "__main__":
    raise SystemExit(main())