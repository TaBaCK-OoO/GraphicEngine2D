import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.utils_quat import rotation_matrix_to_quaternion

if __name__ == '__main__':
    print("=== Завдання 4: Декомпозиція матриці ===")

    R = Mat4x4(
        0, -1, 0, 0,
        1, 0, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    )

    q = rotation_matrix_to_quaternion(R)
    print(f"Кватерніон з матриці: {q}")