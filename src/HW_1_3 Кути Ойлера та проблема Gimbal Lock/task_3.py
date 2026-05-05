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


class Task3Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["cube_xyz"] = Cube(alpha=0.3, color="blue")
        self["cube_zyx"] = Cube(alpha=0.3, color="green")


def print_analytics(M_xyz, M_zyx):
    print("--- Завдання 3: Конвенції та послідовність обертань ---")
    print("\n1. Матриця для конвенції XYZ (зовнішні осі, Rz * Ry * Rx):\n", M_xyz)
    print("\n2. Матриця для конвенції ZYX (зовнішні осі, Rx * Ry * Rz):\n", M_zyx)

    print("\n3. Порівняння координат вершин:")
    for i, v in enumerate(cube_vertices):
        v_xyz = M_xyz * v
        v_zyx = M_zyx * v
        print(f"V{i}: {v[:3]}")
        print(f"   -> XYZ: {v_xyz.xyz}")
        print(f"   -> ZYX: {v_zyx.xyz}")

    print("\nПояснення розбіжності[cite: 96]:")
    print("Множення матриць є некомутативним (A * B != B * A).")
    print("У конвенції XYZ перший поворот (навколо X) змінює просторове розташування")
    print("осей Y та Z. Тому наступні повороти відбуваються вже для об'єкта зі зміненою")
    print("орієнтацією порівняно з конвенцією ZYX, де перший поворот здійснюється навколо осі Z.")
    print("Саме тому фінальна орієнтація куба відрізняється.")


if __name__ == '__main__':
    scene = Task3Scene(
        title="Завдання 3: XYZ vs ZYX",
        coordinate_rect=(-2, -2, -2, 3, 3, 3)
    )

    Rx = Mat4x4.rotation_x(np.radians(45))
    Ry = Mat4x4.rotation_y(np.radians(30))
    Rz = Mat4x4.rotation_z(np.radians(60))

    M_xyz = Rz * Ry * Rx

    M_zyx = Rx * Ry * Rz

    print_analytics(M_xyz, M_zyx)

    anim_xyz = TrsTransformationAnimation(end=M_xyz, channel="cube_xyz")
    anim_zyx = TrsTransformationAnimation(end=M_zyx, channel="cube_zyx")

    scene.add_animations(anim_xyz, anim_zyx)
    scene.show()