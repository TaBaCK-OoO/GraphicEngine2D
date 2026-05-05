import numpy as np

from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4


class Task6Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["cube_orig"] = Cube(alpha=0.1, color="grey", line_style="--")

        cube = Cube(alpha=0.4, color="blue")
        cube.show_local_frame()
        self["cube_interpolated"] = cube


def run_lerp_analysis():
    print("--- Завдання 6: Проблема інтерполяції (Lerp) ---\n")

    look_vector_orig = Vec4(0, 0, 1, 0)
    steps = 10

    angles = np.linspace(0, 90, steps + 1)

    matrices = []

    for i, angle in enumerate(angles):
        rad = np.radians(angle)

        Rx = Mat4x4.rotation_x(rad)
        Ry = Mat4x4.rotation_y(rad)
        Rz = Mat4x4.rotation_z(rad)

        M = Rz * Ry * Rx
        matrices.append(M)
        look_vector_trans = M * look_vector_orig

        print(f"Крок {i} (Кути: {angle:0.1f}°, {angle:0.1f}°, {angle:0.1f}°)")
        print(f"Вектор погляду: {look_vector_trans.xyz}\n")

    print("Пояснення «смиканого» руху:")
    print("При лінійній зміні кутів Ейлера об'єкт не рухається найкоротшим шляхом (по дузі великого кола).")
    print("Коли кут Y наближається до 90 градусів (сингулярність), простір Ейлера сильно викривлюється.")
    print("Щоб компенсувати втрату осі, об'єкт починає виконувати швидкий оберт навколо своєї осі.")
    print("Саме тому в 3D анімації замість Euler Lerp використовують кватерніони (Slerp).")

    return matrices


if __name__ == '__main__':
    matrices = run_lerp_analysis()

    scene = Task6Scene(
        title="Завдання 6: Euler Lerp до Gimbal Lock",
        coordinate_rect=(-2, -2, -2, 3, 3, 3)
    )

    animations = []
    for M in matrices[1:]:
        anim = TrsTransformationAnimation(
            end=M,
            channel="cube_interpolated",
            apply_geometry_transformation_on_finish=True
        )
        animations.append(anim)

    scene.add_animations(*animations)
    scene.show()