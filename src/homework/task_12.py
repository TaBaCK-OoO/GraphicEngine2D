import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import decompose_translation_quaternion_scale, is_orthogonal

matrix_data = [
    [0.707, -0.707, 0, 10],
    [0.707, 0.707, 0, 20],
    [0, 0, 2, 30],
    [0, 0, 0, 1]
]
M = Mat4x4(matrix_data)

translation, quaternion, scale = decompose_translation_quaternion_scale(M)

print(f"Вектор перенесення t: {translation}")
print(f"Масштабні коефіцієнти s: {scale}")

R = quaternion.toRotationMatrix()
print(f"\nМатриця обертання R:\n{np.round(R.data, 3)}")
print(f"Чи є матриця ортогональною? {is_orthogonal(R)}")

trace_R = np.trace(R.data[:3, :3])
angle_rad = np.arccos(np.clip((trace_R - 1) / 2, -1, 1))
angle_deg = np.degrees(angle_rad)

axis_x = R.data[2, 1] - R.data[1, 2]
axis_y = R.data[0, 2] - R.data[2, 0]
axis_z = R.data[1, 0] - R.data[0, 1]
axis = np.array([axis_x, axis_y, axis_z])
axis_unit = axis / np.linalg.norm(axis) if np.linalg.norm(axis) > 1e-6 else [0, 0, 1]

print(f"\nКут повороту: {angle_deg:.2f}°")
print(f"Одиниця осі r: {np.round(axis_unit, 3)}")