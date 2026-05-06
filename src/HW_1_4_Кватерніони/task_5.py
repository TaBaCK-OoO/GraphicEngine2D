import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import decompose_translation_quaternion_scale

if __name__ == '__main__':
    print("=== Завдання 5: Повна декомпозиція афінної матриці ===\n")

    M_np = np.array([
        [0, -2, 0, 10],
        [1, 0, 0, -5],
        [0, 0, 1.5, 3],
        [0, 0, 0, 1]
    ])

    print("--- 1. РУЧНА ДЕКОМПОЗИЦІЯ ---")

    T_manual = M_np[0:3, 3]
    print(f"Вектор перенесення T (tx, ty, tz) = {T_manual}")

    M3x3 = M_np[0:3, 0:3]
    S_manual = np.linalg.norm(M3x3, axis=0)
    print(f"Масштабні коефіцієнти S (sx, sy, sz) = {S_manual}")

    R_manual = M3x3 / S_manual
    print("\nЧиста матриця обертання R:")
    print(R_manual)

    identity_check = np.round(R_manual.dot(R_manual.T), 4)
    is_orthogonal = np.array_equal(identity_check, np.eye(3))
    print(f"Матриця R строго ортогональна? -> {is_orthogonal}\n")

    print("--- 2. ПЕРЕВІРКА РУШІЄМ GraphicEngine3D ---")
    M_engine = Mat4x4(
        0, -2, 0, 10,
        1, 0, 0, -5,
        0, 0, 1.5, 3,
        0, 0, 0, 1
    )

    T_engine, q_engine, S_engine = decompose_translation_quaternion_scale(M_engine)

    print(f"T (рушій) = {T_engine}")
    print(f"S (рушій) = {S_engine}")
    print(f"q (рушій) = {q_engine}")

    print(f"Матриця R (з кватерніона рушія):\n{q_engine.toRotationMatrix()}")
