import numpy as np
from src.math.Quaternion import Quaternion

if __name__ == '__main__':
    print("=== Завдання 3: Конвертація та Gimbal Lock ===\n")

    qx = Quaternion.rotation_x(np.radians(20))
    qy = Quaternion.rotation_y(np.radians(90))
    qz = Quaternion.rotation_z(np.radians(50))

    print(f"qx: {qx}")
    print(f"qy: {qy}")
    print(f"qz: {qz}\n")

    q_final = qz * qy * qx
    print(f"Фінальний кватерніон орієнтації q: {q_final}")

