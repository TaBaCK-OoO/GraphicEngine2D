import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3


def task_0():
    print("=== Завдання 0: Від осі та кута до кватерніона ===")

    theta = np.radians(60)
    u = Vec3(1, 1, 1).normalized()


    q = Quaternion.rotation(theta, u)
    print(f"1. Побудований кватерніон q: {q}")


    norm = q.norm()
    print(f"2. Норма |q| = {norm:.4f} (Одиниця: {np.isclose(norm, 1.0)})")

    R = q.toRotationMatrix()
    print(f"3. Матриця повороту R (Mat4x4):\n{R}")


if __name__ == '__main__':
    task_0()