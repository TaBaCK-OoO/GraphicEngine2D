import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import vertex
from src.math.utils_matrix import decompose_translation_quaternion_scale


def analyze_transformation_matrix(matrix: Mat4x4):

    translation, quaternion, scale = decompose_translation_quaternion_scale(matrix)

    R_obj = quaternion.toRotationMatrix()
    R = R_obj.data[:3, :3]

    trace_R = np.trace(R)
    angle_rad = np.arccos(np.clip((trace_R - 1) / 2, -1, 1))
    angle_deg = np.degrees(angle_rad)

    axis = np.array([
        R[2, 1] - R[1, 2],
        R[0, 2] - R[2, 0],
        R[1, 0] - R[0, 1]
    ])

    norm = np.linalg.norm(axis)
    if norm < 1e-6:
        unit_axis = np.array([1, 0, 0]) if angle_deg < 1.0 else np.array([0, 0, 0])
    else:
        unit_axis = axis / norm

    return {
        "scale": scale,
        "angle_deg": round(angle_deg, 2),
        "axis": np.round(unit_axis, 3),
        "translation": translation
    }


if __name__ == "__main__":
    pivot = Vec3(1, 1, 1)

    M_pivot = Mat4x4.translation(pivot) * Mat4x4.scale(2, 2, 2) * Mat4x4.translation(-pivot)

    M_intrinsic = M_pivot * Mat4x4.rotation_x(np.radians(90))

    M_final = Mat4x4.translation(-3, 4, 2) * M_intrinsic

    results = analyze_transformation_matrix(M_final)

    print("--- Результати декомпозиції Завдання 15 ---")
    print(f"Масштаб (має бути 2.0): {results['scale']}")
    print(f"Кут повороту (має бути 90.0): {results['angle_deg']}°")
    print(f"Вісь повороту (має бути [1, 0, 0]): {results['axis']}")
    print(f"Фінальне зміщення точки (0,0,0): {results['translation']}")

    v_unit = [vertex(0, 0, 0), vertex(1, 1, 1)]
    print("\nПеревірка вершин V0 та V7:")
    print(f"V0 final: {(M_final * v_unit[0]).xyz}")
    print(f"V7 final: {(M_final * v_unit[1]).xyz}")