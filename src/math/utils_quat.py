import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.utils_matrix import is_orthogonal


# ══════════════════════════════════════════════════════════════════════════════
# Кути Ейлера ↔ Кватерніон
# ══════════════════════════════════════════════════════════════════════════════

def euler_to_quaternion(phi, theta, psi, configuration="XYZ"):
    """
    Конвертує кути Ейлера (phi, theta, psi) у одиничний кватерніон для
    заданої конфігурації осей обертання.

    Підтримувані конфігурації Tait-Bryan: XYZ, XZY, YXZ, YZX, ZXY, ZYX
    Підтримувані власні кути Ейлера:     XYX, XZX, YXY, YZY, ZXZ, ZYZ

    Параметри:
        phi, theta, psi : кути у радіанах
        configuration   : рядок з конфігурацією (реєстронечутливий)

    Повертає:
        Quaternion — одиничний кватерніон обертання
    """
    Qx = Quaternion.rotation_x
    Qy = Quaternion.rotation_y
    Qz = Quaternion.rotation_z
    cfg = configuration.upper()

    _map = {
        "XYZ": lambda p, t, s: Qx(p) * Qy(t) * Qz(s),
        "XZY": lambda p, t, s: Qx(p) * Qz(t) * Qy(s),
        "YXZ": lambda p, t, s: Qy(p) * Qx(t) * Qz(s),
        "YZX": lambda p, t, s: Qy(p) * Qz(t) * Qx(s),
        "ZXY": lambda p, t, s: Qz(p) * Qx(t) * Qy(s),
        "ZYX": lambda p, t, s: Qz(p) * Qy(t) * Qx(s),
        "XYX": lambda p, t, s: Qx(p) * Qy(t) * Qx(s),
        "XZX": lambda p, t, s: Qx(p) * Qz(t) * Qx(s),
        "YXY": lambda p, t, s: Qy(p) * Qx(t) * Qy(s),
        "YZY": lambda p, t, s: Qy(p) * Qz(t) * Qy(s),
        "ZXZ": lambda p, t, s: Qz(p) * Qx(t) * Qz(s),
        "ZYZ": lambda p, t, s: Qz(p) * Qy(t) * Qz(s),
    }
    if cfg not in _map:
        raise ValueError(f"Невідома конфігурація Ейлера: '{configuration}'")
    return _map[cfg](phi, theta, psi)


def euler_xyz_to_quaternion(phi, theta, psi):
    """
    Конвертує кути Ейлера XYZ (phi, theta, psi) у одиничний кватерніон.
    Еквівалентно до euler_to_quaternion(phi, theta, psi, "XYZ").

    Використовує прямі аналітичні формули без проміжної матриці обертання.
    """
    cp, sp = np.cos(phi / 2),   np.sin(phi / 2)
    ct, st = np.cos(theta / 2), np.sin(theta / 2)
    cs, ss = np.cos(psi / 2),   np.sin(psi / 2)

    return Quaternion(
        cp * ct * cs - sp * st * ss,
        sp * ct * cs + cp * st * ss,
        cp * st * cs - sp * ct * ss,
        cp * ct * ss + sp * st * cs,
    )


def quaternion_to_euler(quat, configuration="XYZ"):
    """
    Конвертує одиничний кватерніон у кути Ейлера (phi, theta, psi)
    для заданої конфігурації осей обертання.

    Параметри:
        quat          : Quaternion — кватерніон обертання
        configuration : рядок з конфігурацією (реєстронечутливий)

    Повертає:
        (phi, theta, psi) — кути у радіанах
    """
    mat = quat.normalized().toRotationMatrix()
    return mat.toEuler(configuration)


def quaternion_to_euler_xyz(quat):
    """
    Конвертує одиничний кватерніон у кути Ейлера XYZ (phi, theta, psi).
    Використовує прямі аналітичні формули.

    Повертає:
        (phi, theta, psi) — кути у радіанах
    """
    q = quat.normalized()
    w, x, y, z = q.w, q.x, q.y, q.z

    # r[0,2] = 2(xz+wy)
    sin_theta = 2.0 * (w * y + x * z)
    sin_theta = np.clip(sin_theta, -1.0, 1.0)  # захист від чисельних помилок

    theta = np.arcsin(sin_theta)

    # r[1,2] = 2(yz-wx),  r[2,2] = 1-2(x²+y²)
    phi = np.arctan2(2.0 * (w * x - y * z),
                     1.0 - 2.0 * (x * x + y * y))
    # r[0,1] = 2(xy-wz),  r[0,0] = 1-2(y²+z²)
    psi = np.arctan2(2.0 * (w * z - x * y),
                     1.0 - 2.0 * (y * y + z * z))
    return float(phi), float(theta), float(psi)


# ══════════════════════════════════════════════════════════════════════════════
# Матриця обертання ↔ Кватерніон
# ══════════════════════════════════════════════════════════════════════════════

def rotation_matrix_to_quaternion(r):
    """
    Конвертує матрицю обертання у одиничний кватерніон (алгоритм Shepperd).

    Параметри:
        r : ортонормована матриця обертання (Mat4x4, numpy.ndarray або сумісний тип)

    Повертає:
        Quaternion — одиничний кватерніон обертання
    """
    if not is_orthogonal(r):
        raise ValueError("Матриця обертання не є ортогональною!")

    r = Mat4x4(r)
    trace = r[0, 0] + r[1, 1] + r[2, 2]

    if trace >= 0:
        q0 = 0.5 * np.sqrt(1.0 + trace)
        q1 = (r[2, 1] - r[1, 2]) / (4.0 * q0)
        q2 = (r[0, 2] - r[2, 0]) / (4.0 * q0)
        q3 = (r[1, 0] - r[0, 1]) / (4.0 * q0)
    elif (r[0, 0] > r[1, 1]) and (r[0, 0] > r[2, 2]):
        q1 = 0.5 * np.sqrt(1.0 + r[0, 0] - r[1, 1] - r[2, 2])
        q0 = (r[2, 1] - r[1, 2]) / (4.0 * q1)
        q2 = (r[0, 1] + r[1, 0]) / (4.0 * q1)
        q3 = (r[0, 2] + r[2, 0]) / (4.0 * q1)
    elif r[1, 1] > r[2, 2]:
        q2 = 0.5 * np.sqrt(1.0 - r[0, 0] + r[1, 1] - r[2, 2])
        q0 = (r[0, 2] - r[2, 0]) / (4.0 * q2)
        q1 = (r[0, 1] + r[1, 0]) / (4.0 * q2)
        q3 = (r[1, 2] + r[2, 1]) / (4.0 * q2)
    else:
        q3 = 0.5 * np.sqrt(1.0 + r[2, 2] - r[0, 0] - r[1, 1])
        q0 = (r[1, 0] - r[0, 1]) / (4.0 * q3)
        q1 = (r[0, 2] + r[2, 0]) / (4.0 * q3)
        q2 = (r[1, 2] + r[2, 1]) / (4.0 * q3)

    return Quaternion(q0, q1, q2, q3)


def quaternion_to_rotation_matrix(quat):
    """
    Конвертує одиничний кватерніон у матрицю обертання 4×4.

    Параметри:
        quat : Quaternion — кватерніон обертання

    Повертає:
        Mat4x4 — матриця обертання 4×4
    """
    return quat.normalized().toRotationMatrix()


# ══════════════════════════════════════════════════════════════════════════════
# Кут-вісь ↔ Кватерніон
# ══════════════════════════════════════════════════════════════════════════════

def angle_axis_to_quaternion(angle, axis):
    """
    Конвертує представлення обертання «кут-вісь» у кватерніон.

    Параметри:
        angle : кут обертання у радіанах
        axis  : вісь обертання (Vec3, Vec4, list, tuple або numpy.ndarray розміром 3)

    Повертає:
        Quaternion — одиничний кватерніон обертання
    """
    return Quaternion.rotation(angle, axis)


def quaternion_to_angle_axis(quat):
    """
    Конвертує кватерніон у представлення «кут-вісь».

    Параметри:
        quat : Quaternion — кватерніон обертання

    Повертає:
        (angle, axis) де angle у радіанах, axis — Vec3
    """
    return quat.normalized().to_angle_axis()


# ══════════════════════════════════════════════════════════════════════════════
# Інтерполяція кватерніонів
# ══════════════════════════════════════════════════════════════════════════════

def nlerp(q0: Quaternion, q1: Quaternion, t: float) -> Quaternion:
    """
    Нормалізована лінійна інтерполяція (NLERP) між двома кватерніонами.
    Швидша за SLERP, але не є рівномірною по швидкості.

    Параметри:
        q0, q1 : Quaternion — початковий та кінцевий кватерніони
        t      : float — параметр інтерполяції (0 ≤ t ≤ 1)

    Повертає:
        Інтерпольований нормалізований кватерніон
    """
    # Вибір короткого шляху (менше π)
    if quaternion_dot(q0, q1) < 0.0:
        q1 = -q1
    return (q0 * (1.0 - t) + q1 * t).normalized()


def slerp(q0: Quaternion, q1: Quaternion, t: float) -> Quaternion:
    """
    Сферична лінійна інтерполяція (SLERP) між двома кватерніонами.
    Рівномірна по куту, але повільніша за NLERP.

    Параметри:
        q0, q1 : Quaternion — початковий та кінцевий кватерніони
        t      : float — параметр інтерполяції (0 ≤ t ≤ 1)

    Повертає:
        Інтерпольований кватерніон Quaternion
    """
    dot = quaternion_dot(q0, q1)

    # Вибір короткого шляху (менше π)
    if dot < 0.0:
        q1 = -q1
        dot = -dot

    # Якщо кватерніони майже однакові — NLERP для стабільності
    if dot > 0.9995:
        return (q0 * (1.0 - t) + q1 * t).normalized()

    theta_0 = np.arccos(dot)           # кут між кватерніонами
    sin_theta_0 = np.sin(theta_0)

    s0 = np.sin((1.0 - t) * theta_0) / sin_theta_0
    s1 = np.sin(t * theta_0) / sin_theta_0

    return q0 * s0 + q1 * s1


# ══════════════════════════════════════════════════════════════════════════════
# Допоміжні операції над кватерніонами
# ══════════════════════════════════════════════════════════════════════════════

def quaternion_dot(q0: Quaternion, q1: Quaternion) -> float:
    """
    Скалярний добуток двох кватерніонів (розглядає їх як 4D-вектори).

    Повертає:
        float — значення скалярного добутку
    """
    return float(np.dot(q0.q, q1.q))


def are_same_rotation(q0: Quaternion, q1: Quaternion, atol: float = 1e-6) -> bool:
    """
    Перевіряє, чи представляють два кватерніони однакове обертання.
    Враховує подвійне покриття: q та -q задають одне й те саме обертання.

    Параметри:
        q0, q1 : Quaternion — кватерніони для порівняння
        atol   : допустима абсолютна похибка

    Повертає:
        bool
    """
    q0n = q0.normalized()
    q1n = q1.normalized()
    dot = abs(quaternion_dot(q0n, q1n))
    return bool(np.isclose(dot, 1.0, atol=atol))


def angle_between_rotations(q0: Quaternion, q1: Quaternion) -> float:
    """
    Обчислює кут (у радіанах) між двома обертаннями, заданими кватерніонами.
    Геодезична відстань на SO(3).

    Повертає:
        float — кут у радіанах [0, π]
    """
    q0n = q0.normalized()
    q1n = q1.normalized()
    # Відносне обертання: q_rel = q0^(-1) * q1
    q_rel = q0n.inverse() * q1n
    # Кут = 2 * arccos(|w|)
    w = np.clip(abs(q_rel.w), 0.0, 1.0)
    return float(2.0 * np.arccos(w))


def quaternion_identity() -> Quaternion:
    """
    Повертає тривіальний (одиничний) кватерніон, що відповідає нульовому обертанню.

    Повертає:
        Quaternion(1, 0, 0, 0)
    """
    return Quaternion(1.0, 0.0, 0.0, 0.0)


def is_unit_quaternion(quat: Quaternion, atol: float = 1e-6) -> bool:
    """
    Перевіряє, чи є кватерніон одиничним (норма = 1).

    Параметри:
        quat : Quaternion
        atol : допустима абсолютна похибка

    Повертає:
        bool
    """
    return bool(np.isclose(quat.norm(), 1.0, atol=atol))


# ══════════════════════════════════════════════════════════════════════════════
# Приклад використання
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    phi, theta, psi = np.radians(30), np.radians(45), np.radians(60)

    print("=== Euler XYZ → Quaternion ===")
    q_direct = euler_xyz_to_quaternion(phi, theta, psi)
    q_generic = euler_to_quaternion(phi, theta, psi, "XYZ")
    print(f"Direct:  {q_direct}")
    print(f"Generic: {q_generic}")

    print("\n=== Quaternion → Euler XYZ ===")
    recovered = quaternion_to_euler_xyz(q_direct)
    print(f"Recovered angles: {np.degrees(recovered)}")

    print("\n=== Quaternion → Rotation Matrix ===")
    mat = quaternion_to_rotation_matrix(q_direct)
    print(mat)

    print("\n=== Rotation Matrix → Quaternion ===")
    Rx = Mat4x4.rotation_x(phi)
    Ry = Mat4x4.rotation_y(theta)
    Rz = Mat4x4.rotation_z(psi)
    R_final = Rx * Ry * Rz
    q_from_mat = rotation_matrix_to_quaternion(R_final)
    print(f"From matrix: {q_from_mat}")

    print("\n=== SLERP ===")
    q0 = Quaternion.rotation_y(phi)
    q1 = Quaternion.rotation_y(2 * phi)
    for i in range(6):
        t = i / 5
        print(f"  t={t:.2f}: {slerp(q0, q1, t)}")

    print("\n=== NLERP ===")
    for i in range(6):
        t = i / 5
        print(f"  t={t:.2f}: {nlerp(q0, q1, t)}")

    print("\n=== Angle between rotations ===")
    print(f"Angle: {np.degrees(angle_between_rotations(q0, q1)):.4f}°")
