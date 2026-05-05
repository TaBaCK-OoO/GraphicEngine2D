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

    print_explanation()


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


    orig_poly = Polygon(
        rectangle_vertices,
        linewidth=2.0,
        color="grey",
        line_style="--"
    )
    scene.add_figure(orig_poly, "ID_ORIGINAL")

    trans_poly = Polygon(
        rectangle_vertices,
        linewidth=3.0,
        color="red",
        line_style="-"
    )

    T = Mat3x3(
        0.866, 0.5, 4.0,
        0.5, 0.866, 3.0,
        0, 0, 1
    )

    trans_poly.transformation = T
    scene.add_figure(trans_poly, "ID_TRANSFORMED")

    scene.show()