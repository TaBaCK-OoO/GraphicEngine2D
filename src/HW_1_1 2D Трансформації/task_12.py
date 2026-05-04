import numpy as np

from src.engine.scene.Scene import Scene
from src.engine.model.Polygon import Polygon
from src.math.Mat3x3 import Mat3x3

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]


def print_explanation():
    """Виводить аналітичне пояснення для Завдання 12"""
    print("--- Завдання 12: Розкладання матриці ---")
    print("   Розкласти матрицю T на компоненти TRS - НЕМОЖЛИВО.")

    print("   Задана матриця: [0.866,  0.5]")
    print("                   [0.5,  0.866]")
    print("   Елементи побічної діагоналі мають однакові знаки (+0.5).")
    print("   У класичній композиції R * S (Поворот * Масштаб) або S * R,")
    print("   елементи побічної діагоналі мають різні знаки (через -sin та +sin).")
    print("   Рівність знаків свідчить про наявність некласичної деформації (зсуву).")
    print("   Тому функція decompose_affine3 не може виділити ортогональну матрицю повороту.")
    print("-" * 50)


if __name__ == '__main__':
    # Виводимо пояснення в консоль для здачі дз
    print_explanation()

    # Використовуємо статичну Scene, оскільки анімація вимагає валідних TRS компонентів[cite: 12]
    scene = Scene(
        image_size=(8, 8),
        coordinate_rect=(-1, -1, 6, 6),
        title="Завдання 12: Деформація без TRS-декомпозиції",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    # 1. Оригінальний квадрат (0,0) - (1,1)[cite: 4, 12]
    orig_poly = Polygon(
        rectangle_vertices,
        linewidth=2.0,
        color="grey",
        line_style="--"
    )
    scene.add_figure(orig_poly, "ID_ORIGINAL")

    # 2. Трансформований квадрат[cite: 4, 12]
    trans_poly = Polygon(
        rectangle_vertices,
        linewidth=3.0,
        color="red",
        line_style="-"
    )

    # 3. Матриця з умови задачі (Переміщення (4, 3))[cite: 3]
    T = Mat3x3(
        0.866, 0.5, 4.0,
        0.5, 0.866, 3.0,
        0, 0, 1
    )

    # Застосовуємо трансформацію напряму. 
    # Рушій сам перемножить вершини на цю матрицю під час відмальовування[cite: 7, 12]
    trans_poly.transformation = T
    scene.add_figure(trans_poly, "ID_TRANSFORMED")

    scene.show()