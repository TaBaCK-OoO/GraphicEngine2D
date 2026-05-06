import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3
from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.BrokenLine import BrokenLine
from src.engine.animation.QuaternionAnimation import QuaternionAnimation


class TetrahedronScene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vertices = [Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]

        edges_indices = [(0, 1, 2, 0), (0, 3, 1), (3, 2)]

        for i, idxs in enumerate(edges_indices):
            pts = []
            for j in idxs: pts.extend(self.vertices[j].xyz)
            self[f"orig_{i}"] = BrokenLine(*pts, color="grey", linestyle="--", linewidth=1)

        animated_pts = []
        for idxs in edges_indices:
            for j in idxs: animated_pts.extend(self.vertices[j].xyz)

        self["tetra"] = BrokenLine(*animated_pts, color="blue", linewidth=3)


if __name__ == '__main__':
    q1 = Quaternion.rotation_x(np.radians(45))
    q2 = Quaternion.rotation_y(np.radians(30))

    q_total = q2 * q1
    print(f"=== Завдання 2 ===\nРезультуючий кватерніон q_total: {q_total}")

    angle, axis = q_total.to_angle_axis()
    print(f"Сумарний кут: {np.degrees(angle):.2f}°")
    print(f"Вісь обертання: {axis}")

    print("\nНові координати вершин:")
    for i, v in enumerate([Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]):
        v_prime = q_total.rotate_vector(v)
        print(f" V{i}: {v_prime.xyz}")

    scene = TetrahedronScene(title="Завдання 2: Анімація тетраедра", coordinate_rect=(-1, -1, -1, 2, 2, 2))

    anim = QuaternionAnimation(
        end_quaternion=q_total,
        channel="tetra",
        frames=80,
        apply_geometry_transformation_on_finish=True
    )

    scene.add_animations(anim)
    scene.show()