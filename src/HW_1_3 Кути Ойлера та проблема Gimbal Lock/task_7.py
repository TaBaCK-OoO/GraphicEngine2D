import numpy as np

from src.math.Mat4x4 import Mat4x4


def extract_euler_angles(R_mat):

    R = R_mat.data if hasattr(R_mat, 'data') else R_mat

    sin_beta = R[0, 2]
    sin_beta = np.clip(sin_beta, -1.0, 1.0)
    beta = np.arcsin(sin_beta)

    if np.abs(sin_beta) >= 0.9999:
        print("\n[! Виявлено сингулярність (Gimbal Lock) !]")
        print("Втрачено один ступінь вільності. Існує нескінченна кількість комбінацій (alpha, gamma).")

        alpha = 0.0
        print("Алгоритм примусово встановив alpha = 0.")

        gamma = np.arctan2(R[1, 0], R[1, 1])

    else:
        alpha = np.arctan2(-R[1, 2], R[2, 2])
        gamma = np.arctan2(-R[0, 1], R[0, 0])

    return alpha, beta, gamma


def run_task7():
    print("--- Завдання 7: Декомпозиція та неоднозначність розв'язку ---\n")
    R1 = Mat4x4.rotation_z(np.radians(20)) * Mat4x4.rotation_y(np.radians(90)) * Mat4x4.rotation_x(np.radians(40))

    R2 = Mat4x4.rotation_z(np.radians(50)) * Mat4x4.rotation_y(np.radians(90)) * Mat4x4.rotation_x(np.radians(10))

    print("Матриця 1 (alpha=40°, beta=90°, gamma=20°):")
    print(np.round(R1.data[:3, :3], 4))

    print("\nМатриця 2 (alpha=10°, beta=90°, gamma=50°):")
    print(np.round(R2.data[:3, :3], 4))

    print(
        "\nВисновок: Попри різні кути, матриці абсолютно ідентичні. Це доводить наявність нескінченної кількості розв'язків.")

    print("\nЗапуск алгоритму декомпозиції для Матриці 1...")
    a, b, g = extract_euler_angles(R1)

    print(f"\nВідновлені кути (стабільний розв'язок у градусах):")
    print(f"Alpha: {np.degrees(a):.1f}°")
    print(f"Beta:  {np.degrees(b):.1f}°")
    print(f"Gamma: {np.degrees(g):.1f}°")


if __name__ == '__main__':
    run_task7()