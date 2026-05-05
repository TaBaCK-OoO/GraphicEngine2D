import numpy as np

from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4

cube_vertices = [
    np.array([0, 0, 0, 1]), np.array([1, 0, 0, 1]),
    np.array([1, 1, 0, 1]), np.array([0, 1, 0, 1]),
    np.array([0, 0, 1, 1]), np.array([1, 0, 1, 1]),
    np.array([1, 1, 1, 1]), np.array([0, 1, 1, 1])
]


class Task1Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["cube_orig"] = Cube(alpha=0.1, color="grey", line_style="--")
        self["cube_orig"].show_local_frame()
        self["cube_task"] = Cube(alpha=0.3, color="blue")


def print_analytics(S, Rx, Ry, Rz, T, M_final):
    print("--- Завдання 1: Аналітика ---")
    print("1. Матриця розтягу S:\n", S)
    print("2. Матриця обертання X (30°):\n", Rx)
    print("3. Матриця обертання Y (45°):\n", Ry)
    print("4. Матриця обертання Z (60°):\n", Rz)
    print("5. Матриця переміщення T:\n", T)
    print("\nЗагальна матриця трансформації (T * Rz * Ry * Rx * S):\n", M_final)
    print("\nПоложення вершин після всіх трансформацій:")
    for i, v in enumerate(cube_vertices):
        v_trans = M_final * v
        print(f"V{i}: {v[:3]} -> {v_trans.xyz}")


if __name__ == '__main__':
    scene = Task1Scene(
        title="Завдання 1: Розтяг, Обертання, Зсув",
        coordinate_rect=(-5, -2, -2, 5, 5, 8)
    )

    S = Mat4x4.scale(2, 0.5, 1)

    Rx = Mat4x4.rotation_x(np.radians(30))
    Ry = Mat4x4.rotation_y(np.radians(45))
    Rz = Mat4x4.rotation_z(np.radians(60))

    T = Mat4x4.translation(-3, 2, 5)

    M_final = T * Rz * Ry * Rx * S

    print_analytics(S, Rx, Ry, Rz, T, M_final)

    anim = TrsTransformationAnimation(end=M_final, channel="cube_task")
    scene.add_animations(anim)
    scene.show()