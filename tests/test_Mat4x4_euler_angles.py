import numpy as np
import pytest
from scipy.spatial.transform import Rotation as R

from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import is_same_matrix


# ========================  ТЕСТИ ДЛЯ КУТІВ ОЙЛЕРА  ===========================

# 1. Тест обертання XYZ -> повернення до кутів Euler
def test_euler_rotation_xyz():
    angles_orig = (30, 45, 60)  # Градуси
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="xyz")
    recovered_angles = mat.toEuler("XYZ")
    assert np.allclose(np.degrees(recovered_angles), angles_orig, atol=1e-5), "Помилка у відновленні кутів Euler (XYZ)"


# 2. Тест обертання ZXZ -> повернення до кутів Euler
def test_euler_rotation_zxz():
    angles_orig = (90, 45, 30)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="zxz")
    recovered_angles = mat.toEuler("ZXZ")
    assert np.allclose(np.degrees(recovered_angles), angles_orig, atol=1e-5), "Помилка у відновленні кутів Euler (ZXZ)"


# 3. Тест, що обертання на (0,0,0) дає одиничну матрицю
def test_euler_zero_rotation():
    mat = Mat4x4.rotation_euler(0, 0, 0, configuration="xyz")
    expected = Mat4x4.identity()
    assert np.allclose(mat.data, expected.data), "Помилка: очікувалась одинична матриця при обертанні (0,0,0)"


# 4. Тест, що `toEuler()` правильно обробляє одиничну матрицю
def test_toEuler_from_identity():
    mat = Mat4x4.identity()
    angles = mat.toEuler("XYZ")
    expected = (0.0, 0.0, 0.0)
    assert np.allclose(angles, expected), "Помилка у отриманні кутів Euler з одиничної матриці"


# 5. Тест, що `toEuler()` працює після множення обертань
def test_toEuler_after_multiple_rotations():
    phi, theta, psi = np.radians((30, 45, 60))
    mat = (Mat4x4.rotation_euler(phi, 0, 0, "xyz")
           @ Mat4x4.rotation_euler(0, theta, 0, "xyz")
           @ Mat4x4.rotation_euler(0, 0, psi, "xyz"))
    recovered_angles = mat.toEuler("XYZ")
    assert np.allclose(np.degrees(recovered_angles), (30, 45, 60), atol=1e-5), "Помилка у оберненні обертання XYZ"


# 6. Тест некоректного порядку обертання у `rotation_euler()`
def test_invalid_euler_rotation():
    with pytest.raises(ValueError, match="Unknown Euler configuration"):
        Mat4x4.rotation_euler(30, 45, 60, configuration="abc")


# 7. Тест некоректного порядку обертання у `toEuler()`
def test_invalid_toEuler():
    mat = Mat4x4.identity()
    with pytest.raises(ValueError, match="Unknown Euler configuration"):
        mat.toEuler("ABC")


# 8. Тест обернення `rotation_euler()` та `toEuler()`
def test_euler_rotation_and_reversal():
    angles_orig = (10, 20, 30)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="xyz")
    recovered_angles = mat.toEuler("XYZ")
    assert np.allclose(np.degrees(recovered_angles), angles_orig,
                       atol=1e-5), "Помилка у відновленні кутів Euler після обертання"


# 9. Тест для обертань на 180 градусів (можливість двозначності)
def test_euler_180_degree_rotation():
    mat = Mat4x4.rotation_euler(np.radians(180), 0, 0, "xyz")
    recovered_angles = mat.toEuler("XYZ")
    assert np.isclose(np.degrees(recovered_angles[0]), 180, atol=1e-5), "Помилка у відновленні кута 180 градусів"


# 10. Тест для обертання в декількох напрямках і відновлення кутів
def test_euler_complex_rotation():
    phi, theta, psi = np.radians(30), np.radians(45), np.radians(60)
    phi1, theta1, psi1 = np.radians(-30), np.radians(-45), np.radians(-60)
    mat_to = Mat4x4.rotation_euler(phi, theta, psi, "xyz")
    mat_back = Mat4x4.rotation_z(psi1) * Mat4x4.rotation_y(theta1) * Mat4x4.rotation_x(phi1)
    mat = mat_to * mat_back

    recovered_angles = mat.toEuler("XYZ")
    expected = (0, 0, 0)
    assert np.allclose(np.degrees(recovered_angles), expected,
                       atol=1e-5), "Помилка: очікувалось повернення до (0,0,0) після зворотних обертань"


# ========================  ТЕСТИ ДЛЯ КУТІВ ОЙЛЕРА З ЯВНИМИ МАТРИЦЯМИ ===========================

# 1. Тест обертання на 90 градусів навколо X (XYZ)
def test_explicit_rotation_x():
    mat = Mat4x4.rotation_euler(np.radians(90), 0, 0, configuration="xyz")
    expected = np.array([[1, 0, 0, 0],
                         [0, 0, -1, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1]], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), "Помилка у матриці обертання на 90° навколо X"


# 2. Тест обертання на 90 градусів навколо Y (XYZ)
def test_explicit_rotation_y():
    mat = Mat4x4.rotation_euler(0, np.radians(90), 0, configuration="xyz")
    expected = np.array([[0, 0, 1, 0],
                         [0, 1, 0, 0],
                         [-1, 0, 0, 0],
                         [0, 0, 0, 1]], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), "Помилка у матриці обертання на 90° навколо Y"


# 3. Тест обертання на 90 градусів навколо Z (XYZ)
def test_explicit_rotation_z():
    mat = Mat4x4.rotation_euler(0, 0, np.radians(90), configuration="xyz")
    expected = np.array([[0, -1, 0, 0],
                         [1, 0, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), "Помилка у матриці обертання на 90° навколо Z"


# 4. Тест обертання на 45 градусів навколо XYZ (комбіноване обертання)
def test_explicit_rotation_xyz():
    phi, theta, psi = np.radians(45), np.radians(45), np.radians(45),
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="xyz")
    expected = np.array([[0.5, -0.5, 0.70710678, 0],
                         [0.85355339, 0.14644661, -0.5, 0],
                         [0.14644661, 0.85355339, 0.5, 0],
                         [0, 0, 0, 1]], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), "Помилка у матриці обертання (45°, 45°, 45°)"


# 4. Тест обертання на 45 градусів навколо XYZ (комбіноване обертання)
def test_explicit_rotation_xyz2():
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="xyz")
    expected = Mat4x4([
        [0.35355339, -0.61237244, 0.70710678, 0],
        [0.9267767, 0.12682648, -0.35355339, 0],
        [0.12682648, 0.78033009, 0.61237244, 0],
        [0, 0, 0, 1],
    ])

    assert is_same_matrix(mat.data, expected), "Помилка у матриці обертання (30°, 45°, 60°)"


# 5. Тест обертання на 30 градусів у конфігурації ZXZ
def test_explicit_rotation_zxz():
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="ZXZ")

    # Виправлена очікувана матриця для ZXZ
    expected = np.array(
        [[0.12682648, -0.9267767, 0.35355339, 0],
         [0.78033009, -0.12682648, -0.61237244, 0],
         [0.61237244, 0.35355339, 0.70710678, 0],
         [0, 0, 0, 1]]
        , dtype=float)

    assert np.allclose(mat.data, expected, atol=1e-5), "Помилка у матриці обертання ZXZ (30°, 45°, 60°)"


# ========================  ТЕСТИ ДЛЯ НОВИХ КОНФІГУРАЦІЙ TAIT-BRYAN  ==========

# ── XZY ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_xzy_roundtrip():
    """XZY: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="XZY")
    recovered = mat.toEuler("XZY")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (XZY)"


def test_euler_rotation_xzy_zero():
    """XZY: обертання (0,0,0) → одинична матриця."""
    mat = Mat4x4.rotation_euler(0, 0, 0, configuration="XZY")
    assert np.allclose(mat.data, Mat4x4.identity().data), \
        "Помилка: очікувалась одинична матриця при обертанні (0,0,0) XZY"


def test_toEuler_xzy_from_identity():
    """XZY: одинична матриця → кути (0,0,0)."""
    angles = Mat4x4.identity().toEuler("XZY")
    assert np.allclose(angles, (0.0, 0.0, 0.0)), \
        "Помилка у отриманні кутів Euler (XZY) з одиничної матриці"


def test_explicit_rotation_xzy():
    """XZY: явна перевірка матриці обертання Rx(30°)*Rz(45°)*Ry(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="XZY")
    expected = np.array([
        [ 0.35355339, -0.70710678,  0.61237244, 0],
        [ 0.73919892,  0.61237244,  0.28033009, 0],
        [-0.57322330,  0.35355339,  0.73919892, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання XZY (30°, 45°, 60°)"


# ── YXZ ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_yxz_roundtrip():
    """YXZ: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="YXZ")
    recovered = mat.toEuler("YXZ")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (YXZ)"


def test_euler_rotation_yxz_zero():
    """YXZ: обертання (0,0,0) → одинична матриця."""
    mat = Mat4x4.rotation_euler(0, 0, 0, configuration="YXZ")
    assert np.allclose(mat.data, Mat4x4.identity().data), \
        "Помилка: очікувалась одинична матриця при обертанні (0,0,0) YXZ"


def test_toEuler_yxz_from_identity():
    """YXZ: одинична матриця → кути (0,0,0)."""
    angles = Mat4x4.identity().toEuler("YXZ")
    assert np.allclose(angles, (0.0, 0.0, 0.0)), \
        "Помилка у отриманні кутів Euler (YXZ) з одиничної матриці"


def test_explicit_rotation_yxz():
    """YXZ: явна перевірка матриці обертання Ry(30°)*Rx(45°)*Rz(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="YXZ")
    expected = np.array([
        [ 0.73919892, -0.57322330,  0.35355339, 0],
        [ 0.61237244,  0.35355339, -0.70710678, 0],
        [ 0.28033009,  0.73919892,  0.61237244, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання YXZ (30°, 45°, 60°)"


# ── YZX ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_yzx_roundtrip():
    """YZX: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="YZX")
    recovered = mat.toEuler("YZX")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (YZX)"


def test_euler_rotation_yzx_zero():
    """YZX: обертання (0,0,0) → одинична матриця."""
    mat = Mat4x4.rotation_euler(0, 0, 0, configuration="YZX")
    assert np.allclose(mat.data, Mat4x4.identity().data), \
        "Помилка: очікувалась одинична матриця при обертанні (0,0,0) YZX"


def test_toEuler_yzx_from_identity():
    """YZX: одинична матриця → кути (0,0,0)."""
    angles = Mat4x4.identity().toEuler("YZX")
    assert np.allclose(angles, (0.0, 0.0, 0.0)), \
        "Помилка у отриманні кутів Euler (YZX) з одиничної матриці"


def test_explicit_rotation_yzx():
    """YZX: явна перевірка матриці обертання Ry(30°)*Rz(45°)*Rx(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="YZX")
    expected = np.array([
        [ 0.61237244,  0.12682648,  0.78033009, 0],
        [ 0.70710678,  0.35355339, -0.61237244, 0],
        [-0.35355339,  0.92677670,  0.12682648, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання YZX (30°, 45°, 60°)"


# ── ZXY ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_zxy_roundtrip():
    """ZXY: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="ZXY")
    recovered = mat.toEuler("ZXY")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (ZXY)"


def test_euler_rotation_zxy_zero():
    """ZXY: обертання (0,0,0) → одинична матриця."""
    mat = Mat4x4.rotation_euler(0, 0, 0, configuration="ZXY")
    assert np.allclose(mat.data, Mat4x4.identity().data), \
        "Помилка: очікувалась одинична матриця при обертанні (0,0,0) ZXY"


def test_toEuler_zxy_from_identity():
    """ZXY: одинична матриця → кути (0,0,0)."""
    angles = Mat4x4.identity().toEuler("ZXY")
    assert np.allclose(angles, (0.0, 0.0, 0.0)), \
        "Помилка у отриманні кутів Euler (ZXY) з одиничної матриці"


def test_explicit_rotation_zxy():
    """ZXY: явна перевірка матриці обертання Rz(30°)*Rx(45°)*Ry(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="ZXY")
    expected = np.array([
        [ 0.12682648, -0.35355339,  0.92677670, 0],
        [ 0.78033009,  0.61237244,  0.12682648, 0],
        [-0.61237244,  0.70710678,  0.35355339, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання ZXY (30°, 45°, 60°)"


# ── ZYX ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_zyx_roundtrip():
    """ZYX (yaw-pitch-roll): rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="ZYX")
    recovered = mat.toEuler("ZYX")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (ZYX)"


def test_euler_rotation_zyx_zero():
    """ZYX: обертання (0,0,0) → одинична матриця."""
    mat = Mat4x4.rotation_euler(0, 0, 0, configuration="ZYX")
    assert np.allclose(mat.data, Mat4x4.identity().data), \
        "Помилка: очікувалась одинична матриця при обертанні (0,0,0) ZYX"


def test_toEuler_zyx_from_identity():
    """ZYX: одинична матриця → кути (0,0,0)."""
    angles = Mat4x4.identity().toEuler("ZYX")
    assert np.allclose(angles, (0.0, 0.0, 0.0)), \
        "Помилка у отриманні кутів Euler (ZYX) з одиничної матриці"


def test_explicit_rotation_zyx():
    """ZYX: явна перевірка матриці обертання Rz(30°)*Ry(45°)*Rx(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="ZYX")
    expected = np.array([
        [ 0.61237244,  0.28033009,  0.73919892, 0],
        [ 0.35355339,  0.73919892, -0.57322330, 0],
        [-0.70710678,  0.61237244,  0.35355339, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання ZYX (30°, 45°, 60°)"


def test_zyx_inverse_rotation():
    """ZYX: R * R^(-1) = I (обернена матриця дорівнює транспонованій для обертань)."""
    phi, theta, psi = np.radians(30), np.radians(45), np.radians(60)
    mat = Mat4x4.rotation_euler(phi, theta, psi, "ZYX")
    # Обернена матриця обертання = транспонована
    mat_inv = mat.inverse()
    result = mat * mat_inv
    assert np.allclose(result.data, Mat4x4.identity().data, atol=1e-5), \
        "Помилка: ZYX R * R^(-1) не дає одиничної матриці"
    # Додатково: для ZYX обернена є XYZ(-psi, -theta, -phi)
    mat_back_correct = (Mat4x4.rotation_x(-psi)
                        * Mat4x4.rotation_y(-theta)
                        * Mat4x4.rotation_z(-phi))
    result2 = mat * mat_back_correct
    assert np.allclose(result2.data, Mat4x4.identity().data, atol=1e-5), \
        "Помилка: ZYX обернена (Rx*Ry*Rz із зворотніми кутами) не дає одиничної матриці"


# ========================  ТЕСТИ ДЛЯ ВЛАСНИХ КУТІВ ЕЙЛЕРА  ===================

# ── XYX ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_xyx_roundtrip():
    """XYX: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="XYX")
    recovered = mat.toEuler("XYX")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (XYX)"


def test_toEuler_xyx_from_identity():
    """XYX: одинична матриця → theta=0 (phi та psi невизначені, але theta=0)."""
    mat = Mat4x4.identity()
    _, theta, _ = mat.toEuler("XYX")
    assert np.isclose(theta, 0.0), \
        "Помилка: XYX theta одиничної матриці має бути 0"


def test_explicit_rotation_xyx():
    """XYX: явна перевірка матриці обертання Rx(30°)*Ry(45°)*Rx(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="XYX")
    expected = np.array([
        [ 0.70710678,  0.61237244,  0.35355339, 0],
        [ 0.35355339,  0.12682648, -0.92677670, 0],
        [-0.61237244,  0.78033009, -0.12682648, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання XYX (30°, 45°, 60°)"


# ── XZX ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_xzx_roundtrip():
    """XZX: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="XZX")
    recovered = mat.toEuler("XZX")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (XZX)"


def test_toEuler_xzx_from_identity():
    """XZX: одинична матриця → theta=0."""
    mat = Mat4x4.identity()
    _, theta, _ = mat.toEuler("XZX")
    assert np.isclose(theta, 0.0), \
        "Помилка: XZX theta одиничної матриці має бути 0"


def test_explicit_rotation_xzx():
    """XZX: явна перевірка матриці обертання Rx(30°)*Rz(45°)*Rx(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="XZX")
    expected = np.array([
        [ 0.70710678, -0.35355339,  0.61237244, 0],
        [ 0.61237244, -0.12682648, -0.78033009, 0],
        [ 0.35355339,  0.92677670,  0.12682648, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання XZX (30°, 45°, 60°)"


# ── YXY ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_yxy_roundtrip():
    """YXY: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="YXY")
    recovered = mat.toEuler("YXY")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (YXY)"


def test_toEuler_yxy_from_identity():
    """YXY: одинична матриця → theta=0."""
    mat = Mat4x4.identity()
    _, theta, _ = mat.toEuler("YXY")
    assert np.isclose(theta, 0.0), \
        "Помилка: YXY theta одиничної матриці має бути 0"


def test_explicit_rotation_yxy():
    """YXY: явна перевірка матриці обертання Ry(30°)*Rx(45°)*Ry(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="YXY")
    expected = np.array([
        [ 0.12682648,  0.35355339,  0.92677670, 0],
        [ 0.61237244,  0.70710678, -0.35355339, 0],
        [-0.78033009,  0.61237244, -0.12682648, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання YXY (30°, 45°, 60°)"


# ── YZY ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_yzy_roundtrip():
    """YZY: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="YZY")
    recovered = mat.toEuler("YZY")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (YZY)"


def test_toEuler_yzy_from_identity():
    """YZY: одинична матриця → theta=0."""
    mat = Mat4x4.identity()
    _, theta, _ = mat.toEuler("YZY")
    assert np.isclose(theta, 0.0), \
        "Помилка: YZY theta одиничної матриці має бути 0"


def test_explicit_rotation_yzy():
    """YZY: явна перевірка матриці обертання Ry(30°)*Rz(45°)*Ry(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="YZY")
    expected = np.array([
        [-0.12682648, -0.61237244,  0.78033009, 0],
        [ 0.35355339,  0.70710678,  0.61237244, 0],
        [-0.92677670,  0.35355339,  0.12682648, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання YZY (30°, 45°, 60°)"


# ── ZYZ ──────────────────────────────────────────────────────────────────────

def test_euler_rotation_zyz_roundtrip():
    """ZYZ: rotation_euler → toEuler повертає вихідні кути."""
    angles_orig = (30, 45, 60)
    angles = np.radians(angles_orig)
    mat = Mat4x4.rotation_euler(*angles, configuration="ZYZ")
    recovered = mat.toEuler("ZYZ")
    assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
        "Помилка у відновленні кутів Euler (ZYZ)"


def test_toEuler_zyz_from_identity():
    """ZYZ: одинична матриця → theta=0."""
    mat = Mat4x4.identity()
    _, theta, _ = mat.toEuler("ZYZ")
    assert np.isclose(theta, 0.0), \
        "Помилка: ZYZ theta одиничної матриці має бути 0"


def test_explicit_rotation_zyz():
    """ZYZ: явна перевірка матриці обертання Rz(30°)*Ry(45°)*Rz(60°)."""
    phi, theta, psi = np.radians((30, 45, 60))
    mat = Mat4x4.rotation_euler(phi, theta, psi, configuration="ZYZ")
    expected = np.array([
        [-0.12682648, -0.78033009,  0.61237244, 0],
        [ 0.92677670,  0.12682648,  0.35355339, 0],
        [-0.35355339,  0.61237244,  0.70710678, 0],
        [ 0,           0,           0,          1],
    ], dtype=float)
    assert np.allclose(mat.data, expected, atol=1e-5), \
        "Помилка у матриці обертання ZYZ (30°, 45°, 60°)"


# ========================  ЗАГАЛЬНІ ТЕСТИ ДЛЯ ВСІХ КОНФІГУРАЦІЙ  =============

TAIT_BRYAN_CONFIGS = ["XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"]
PROPER_EULER_CONFIGS = ["XYX", "XZX", "YXY", "YZY", "ZXZ", "ZYZ"]
ALL_CONFIGS = TAIT_BRYAN_CONFIGS + PROPER_EULER_CONFIGS


def test_all_configs_zero_gives_identity():
    """Усі конфігурації: обертання (0,0,0) → одинична матриця."""
    for cfg in ALL_CONFIGS:
        mat = Mat4x4.rotation_euler(0, 0, 0, configuration=cfg)
        assert np.allclose(mat.data, Mat4x4.identity().data, atol=1e-5), \
            f"Помилка: {cfg} (0,0,0) не дає одиничної матриці"


def test_all_configs_roundtrip():
    """Усі конфігурації: round-trip rotation_euler → toEuler для кутів (10°, 20°, 30°)."""
    angles_orig = (10, 20, 30)
    angles = np.radians(angles_orig)
    for cfg in ALL_CONFIGS:
        mat = Mat4x4.rotation_euler(*angles, configuration=cfg)
        recovered = mat.toEuler(cfg)
        assert np.allclose(np.degrees(recovered), angles_orig, atol=1e-5), \
            f"Помилка у round-trip тесті для конфігурації {cfg}"


def test_all_configs_result_is_rotation_matrix():
    """Усі конфігурації: результуюча матриця є ортогональною з det=1."""
    angles = np.radians((30, 45, 60))
    for cfg in ALL_CONFIGS:
        mat = Mat4x4.rotation_euler(*angles, configuration=cfg)
        r = mat.data[:3, :3]
        assert np.allclose(r @ r.T, np.eye(3), atol=1e-5), \
            f"{cfg}: матриця не є ортогональною"
        assert np.isclose(np.linalg.det(r), 1.0, atol=1e-5), \
            f"{cfg}: det матриці обертання не дорівнює 1"


def test_all_configs_case_insensitive():
    """Усі конфігурації: регістр рядка не важливий."""
    angles = np.radians((30, 45, 60))
    for cfg in ALL_CONFIGS:
        mat_upper = Mat4x4.rotation_euler(*angles, configuration=cfg.upper())
        mat_lower = Mat4x4.rotation_euler(*angles, configuration=cfg.lower())
        assert np.allclose(mat_upper.data, mat_lower.data, atol=1e-5), \
            f"{cfg}: результати для верхнього та нижнього регістру відрізняються"
