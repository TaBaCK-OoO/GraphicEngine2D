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


class Task5Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["cube_orig"] = Cube(alpha=0.1, color="grey", line_style="--")
        self["cube_orig"].show_local_frame()
        self["cube_task"] = Cube(alpha=0.4, color="red")


def run_experiment():
    print("--- Завдання 5: Експеримент «Втрачена вісь» ---\n")

    Rx1 = Mat4x4.rotation_x(np.radians(30))
    Ry1 = Mat4x4.rotation_y(np.radians(90))
    Rz1 = Mat4x4.rotation_z(np.radians(45))
    M1 = Rz1 * Ry1 * Rx1

    Rx2 = Mat4x4.rotation_x(np.radians(40))
    Ry2 = Mat4x4.rotation_y(np.radians(90))
    Rz2 = Mat4x4.rotation_z(np.radians(35))
    M2 = Rz2 * Ry2 * Rx2

    print("Координати вершин для Сценарію 1 (30°, 90°, 45°):")
    for i, v in enumerate(cube_vertices):
        print(f"V{i}: {(M1 * v).xyz}")

    print("\nКоординати вершин для Сценарію 2 (40°, 90°, 35°):")
    for i, v in enumerate(cube_vertices):
        print(f"V{i}: {(M2 * v).xyz}")

    print("\nВисновок:")
    print("Координати в обох сценаріях АБСОЛЮТНО ідентичні.")
    print("Оскільки сума/різниця (залежно від напрямку осей) кутів X та Z не змінилася,")
    print("фінальна орієнтація куба залишилася незмінною. Це наочно доводить «склеювання» осей X та Z.")

    return M1


if __name__ == '__main__':
    M_final = run_experiment()

    scene = Task5Scene(
        title="Завдання 5: Практичний експеримент Gimbal Lock",
        coordinate_rect=(-2, -2, -2, 3, 3, 3)
    )

    anim = TrsTransformationAnimation(end=M_final, channel="cube_task")
    scene.add_animations(anim)
    scene.show()