import turtle # для малювання фракталів 
import argparse # для парсингу аргументів командного рядка 
import sys

MAX_LEVEL = 6  # максимальний рівень рекурсії

def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)

def draw_koch_snowflake(order, size=300):
    # коефіцієнт збільшення фігури в залежності від рівня
    scale_factor = 1.2 + order * 0.3
    window_size = int(size * scale_factor)

    window = turtle.Screen() # налаштування вікна turtle графіки
    window.setup(width=window_size + 100, height=window_size + 100)
    window.screensize(window_size, window_size)
    window.bgcolor("white")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # прискорення анімації на рівнях > 3
    fast_mode = order > 3
    if fast_mode:
        window.tracer(0, 0)  # вимикаємо анімацію

    # розрахунок початкової позиції
    t.penup()
    t.goto(-size / 2, size / (2 * 1.7))  # трохи вище середини
    t.pendown()

    for _ in range(3): # малюємо три сторони сніжинки Коха 
        koch_curve(t, order, size)
        t.right(120)

    if fast_mode:  # якщо швидкий режим — оновлюємо екран один раз в кінці
        window.update() 
        
    window.exitonclick() # чекаємо кліку для закриття вікна 

def validate_level(level: int) -> int:
    if 0 <= level <= MAX_LEVEL:
        return level
    print(f"[ПОПЕРЕДЖЕННЯ] Рівень {level} недопустимий. Використовую рівень 3.")
    return 3

def main():
    parser = argparse.ArgumentParser(description="Малювання фракталу 'Сніжинка Коха'")
    parser.add_argument("--level", "-l", type=int, help="Рівень рекурсії (0–6)")
    parser.add_argument("--size", "-s", type=int, default=300, help="Розмір сторони (за замовчуванням 300)")
    args = parser.parse_args()

    if args.level is None:
        try:
            user_input = int(input(f"Введіть рівень рекурсії (наприклад, 0–{MAX_LEVEL}): "))
        except ValueError:
            print("[ПОПЕРЕДЖЕННЯ] Некоректне значення. Використовую рівень 3.")
            user_input = 3
        level = validate_level(user_input)
    else:
        level = validate_level(args.level)

    draw_koch_snowflake(level, args.size)

if __name__ == "__main__":
    sys.exit(main())
