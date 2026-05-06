import numpy as np

from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3
from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Vector import Vector
from src.engine.model.CoordinateFrame import CoordinateFrame
from src.engine.animation.QuaternionAnimation import QuaternionAnimation

if __name__ == '__main__':
    print("=== Завдання 1: Операція повороту вектора (з анімацією) ===\n")

    p = Vec3(1, 0, 0)
    angle = np.radians(90)

    # Створення кватерніона за допомогою рушія
    q = Quaternion.rotation_z(angle)

    p_prime = q.rotate_vector(p)
    print(f"Початковий вектор: {p.xyz}")
    print(f"Кватерніон повороту q: {q}")
    print(f"Результат повороту: {p_prime.xyz}")

    scene = AnimatedScene(
        title="Завдання 1: Анімація повороту вектора p(1,0,0) на 90°",
        coordinate_rect=(-1.5, -1.5, -1.5, 1.5, 1.5, 1.5),
        base_axis_show=False,
        axis_show=False
    )


    scene["coord_axes"] = CoordinateFrame()

    scene["original_p"] = Vector(0, 0, 0, *p.xyz, color="grey", linestyle="--", linewidth=2)

    scene["animated_p"] = Vector(0, 0, 0, *p.xyz, color="red", linewidth=4)

    anim = QuaternionAnimation(
        end_quaternion=q,
        channel="animated_p",
        frames=60,
        apply_geometry_transformation_on_finish=True
    )

    scene.add_animations(anim)
    scene.show()