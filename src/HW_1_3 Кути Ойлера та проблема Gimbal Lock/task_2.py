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

class Task2Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["cube_orig"] = Cube(alpha=0.1, color="grey", line_style="--")
        self["cube_orig"].show_local_frame()
        self["cube_task"] = Cube(alpha=0.3, color="red")

def print_analytics(Rz, Ry, Rx, T, M_final):
    print("--- Завдання 2: Аналітика ---")
    print("1. Матриця обертання Z (20°):\n", Rz)
    print("2. Матриця обертання Y (35°):\n", Ry)
    print("3. Матриця обертання X (50°):\n", Rx)
    print("4. Матриця переміщення T:\n", T)
    print("\nЗагальна матриця трансформації (ZYX: T * Rx * Ry * Rz):\n", M_final)
    print("\nПоложення вершин після всіх трансформацій:")
    for i, v in enumerate(cube_vertices):
        v_trans = M_final * v
        print(f"V{i}: {v[:3]} -> {v_trans.xyz}")

if __name__ == '__main__':
    scene = Task2Scene(title="Завдання 2: Поворот ZYX", coordinate_rect=(-2, -2, -4, 4, 6, 4))

    Rz = Mat4x4.rotation_z(np.radians(20))
    Ry = Mat4x4.rotation_y(np.radians(35))
    Rx = Mat4x4.rotation_x(np.radians(50))

    T = Mat4x4.translation(1, 3, -2)

    M_final = T * Rx * Ry * Rz

    print_analytics(Rz, Ry, Rx, T, M_final)

    anim = TrsTransformationAnimation(end=M_final, channel="cube_task")
    scene.add_animations(anim)
    scene.show()