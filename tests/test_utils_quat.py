import numpy as np
import pytest

from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3
from src.math.utils_quat import (
    euler_to_quaternion,
    euler_xyz_to_quaternion,
    quaternion_to_euler,
    quaternion_to_euler_xyz,
    rotation_matrix_to_quaternion,
    quaternion_to_rotation_matrix,
    angle_axis_to_quaternion,
    quaternion_to_angle_axis,
    slerp,
    nlerp,
    quaternion_dot,
    are_same_rotation,
    angle_between_rotations,
    quaternion_identity,
    is_unit_quaternion,
)

ALL_CONFIGS = [
    "XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX",
    "XYX", "XZX", "YXY", "YZY", "ZXZ", "ZYZ",
]


# ══════════════════════════════════════════════════════════════════════════════
# Кути Ейлера → Кватерніон
# ══════════════════════════════════════════════════════════════════════════════

class TestEulerToQuaternion:

    def test_xyz_direct_vs_generic(self):
        """euler_xyz_to_quaternion та euler_to_quaternion('XYZ') дають однаковий результат."""
        phi, theta, psi = np.radians((30, 45, 60))
        q_direct = euler_xyz_to_quaternion(phi, theta, psi)
        q_generic = euler_to_quaternion(phi, theta, psi, "XYZ")
        assert np.allclose(q_direct.q, q_generic.q, atol=1e-10)

    def test_zero_angles_give_identity(self):
        """Кути (0,0,0) для будь-якої конфігурації дають одиничний кватерніон."""
        for cfg in ALL_CONFIGS:
            q = euler_to_quaternion(0.0, 0.0, 0.0, cfg)
            assert np.allclose(q.q, [1, 0, 0, 0], atol=1e-10), \
                f"{cfg}: (0,0,0) має давати одиничний кватерніон"

    def test_result_is_unit_quaternion(self):
        """Результат euler_to_quaternion завжди є одиничним кватерніоном."""
        angles = np.radians((30, 45, 60))
        for cfg in ALL_CONFIGS:
            q = euler_to_quaternion(*angles, cfg)
            assert is_unit_quaternion(q, atol=1e-6), \
                f"{cfg}: результат має бути одиничним кватерніоном"

    def test_case_insensitive(self):
        """Конфігурація реєстронечутлива."""
        angles = np.radians((20, 35, 50))
        for cfg in ALL_CONFIGS:
            q_upper = euler_to_quaternion(*angles, cfg.upper())
            q_lower = euler_to_quaternion(*angles, cfg.lower())
            assert np.allclose(q_upper.q, q_lower.q, atol=1e-10), \
                f"{cfg}: верхній і нижній регістр дають різні результати"

    def test_invalid_configuration(self):
        """Невідома конфігурація піднімає ValueError."""
        with pytest.raises(ValueError):
            euler_to_quaternion(0.1, 0.2, 0.3, "ABC")

    def test_xyz_single_axis_x(self):
        """XYZ з theta=psi=0: має відповідати Quaternion.rotation_x."""
        phi = np.radians(45)
        q_expected = Quaternion.rotation_x(phi)
        q = euler_to_quaternion(phi, 0.0, 0.0, "XYZ")
        assert are_same_rotation(q, q_expected)

    def test_xyz_single_axis_y(self):
        """XYZ з phi=psi=0: має відповідати Quaternion.rotation_y."""
        theta = np.radians(45)
        q_expected = Quaternion.rotation_y(theta)
        q = euler_to_quaternion(0.0, theta, 0.0, "XYZ")
        assert are_same_rotation(q, q_expected)

    def test_xyz_single_axis_z(self):
        """XYZ з phi=theta=0: має відповідати Quaternion.rotation_z."""
        psi = np.radians(45)
        q_expected = Quaternion.rotation_z(psi)
        q = euler_to_quaternion(0.0, 0.0, psi, "XYZ")
        assert are_same_rotation(q, q_expected)

    def test_zyx_matches_component_product(self):
        """ZYX: Qz(phi)*Qy(theta)*Qx(psi) = euler_to_quaternion(..., 'ZYX')."""
        phi, theta, psi = np.radians((30, 45, 60))
        q_expected = (Quaternion.rotation_z(phi)
                      * Quaternion.rotation_y(theta)
                      * Quaternion.rotation_x(psi))
        q = euler_to_quaternion(phi, theta, psi, "ZYX")
        assert are_same_rotation(q, q_expected)


# ══════════════════════════════════════════════════════════════════════════════
# Кватерніон → Кути Ейлера (round-trip)
# ══════════════════════════════════════════════════════════════════════════════

class TestQuaternionToEuler:

    def test_xyz_direct_vs_generic(self):
        """quaternion_to_euler_xyz та quaternion_to_euler('XYZ') дають однаковий результат."""
        q = euler_xyz_to_quaternion(*np.radians((30, 45, 60)))
        angles_direct = quaternion_to_euler_xyz(q)
        angles_generic = quaternion_to_euler(q, "XYZ")
        assert np.allclose(angles_direct, angles_generic, atol=1e-6)

    def test_roundtrip_all_configs(self):
        """Round-trip euler→quaternion→euler для всіх конфігурацій."""
        angles_orig = np.radians((30, 45, 60))
        for cfg in ALL_CONFIGS:
            q = euler_to_quaternion(*angles_orig, cfg)
            recovered = quaternion_to_euler(q, cfg)
            assert np.allclose(np.degrees(recovered), np.degrees(angles_orig), atol=1e-5), \
                f"{cfg}: round-trip кутів не вдався"

    def test_roundtrip_various_angles(self):
        """Round-trip для різних кутів у XYZ."""
        test_angles = [
            (10, 20, 30),
            (-45, 30, 90),
            (90, 0, 0),
            (0, 90, 0),
            (0, 0, 90),
        ]
        for deg in test_angles:
            angles = np.radians(deg)
            q = euler_xyz_to_quaternion(*angles)
            recovered = quaternion_to_euler_xyz(q)
            assert np.allclose(np.degrees(recovered), deg, atol=1e-5), \
                f"Round-trip для {deg} не вдався"

    def test_identity_quaternion_gives_zero_angles(self):
        """Одиничний кватерніон → (0, 0, 0) для всіх Tait-Bryan конфігурацій."""
        q = quaternion_identity()
        for cfg in ["XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"]:
            angles = quaternion_to_euler(q, cfg)
            assert np.allclose(angles, (0.0, 0.0, 0.0), atol=1e-10), \
                f"{cfg}: одиничний кватерніон має давати (0,0,0)"

    def test_negative_quaternion_same_rotation(self):
        """q та -q задають одне й те саме обертання → однакові кути Ейлера."""
        q = euler_xyz_to_quaternion(*np.radians((30, 45, 60)))
        angles_pos = quaternion_to_euler_xyz(q)
        angles_neg = quaternion_to_euler_xyz(-q)
        assert np.allclose(angles_pos, angles_neg, atol=1e-6)


# ══════════════════════════════════════════════════════════════════════════════
# Матриця обертання ↔ Кватерніон
# ══════════════════════════════════════════════════════════════════════════════

class TestRotationMatrixQuaternion:

    def test_matrix_to_quaternion_and_back(self):
        """rotation_matrix → quaternion → rotation_matrix дає вихідну матрицю."""
        phi, theta, psi = np.radians((30, 45, 60))
        mat = Mat4x4.rotation_euler(phi, theta, psi, "XYZ")
        q = rotation_matrix_to_quaternion(mat)
        mat_recovered = quaternion_to_rotation_matrix(q)
        assert np.allclose(mat.data, mat_recovered.data, atol=1e-6)

    def test_quaternion_to_matrix_and_back(self):
        """quaternion → rotation_matrix → quaternion дає вихідний кватерніон (з точністю до знаку)."""
        q = euler_to_quaternion(*np.radians((30, 45, 60)), "XYZ")
        mat = quaternion_to_rotation_matrix(q)
        q_recovered = rotation_matrix_to_quaternion(mat)
        assert are_same_rotation(q, q_recovered)

    def test_identity_matrix_gives_identity_quaternion(self):
        """Одинична матриця → одиничний кватерніон."""
        q = rotation_matrix_to_quaternion(Mat4x4.identity())
        assert are_same_rotation(q, quaternion_identity())

    def test_rotation_x_90(self):
        """Rx(90°) дає кватерніон (cos45°, sin45°, 0, 0)."""
        mat = Mat4x4.rotation_x(np.radians(90))
        q = rotation_matrix_to_quaternion(mat)
        q_expected = Quaternion.rotation_x(np.radians(90))
        assert are_same_rotation(q, q_expected)

    def test_rotation_y_90(self):
        """Ry(90°) дає кватерніон (cos45°, 0, sin45°, 0)."""
        mat = Mat4x4.rotation_y(np.radians(90))
        q = rotation_matrix_to_quaternion(mat)
        q_expected = Quaternion.rotation_y(np.radians(90))
        assert are_same_rotation(q, q_expected)

    def test_rotation_z_90(self):
        """Rz(90°) дає кватерніон (cos45°, 0, 0, sin45°)."""
        mat = Mat4x4.rotation_z(np.radians(90))
        q = rotation_matrix_to_quaternion(mat)
        q_expected = Quaternion.rotation_z(np.radians(90))
        assert are_same_rotation(q, q_expected)

    def test_non_orthogonal_matrix_raises(self):
        """Не-ортогональна матриця піднімає ValueError."""
        bad_mat = Mat4x4(2, 0, 0, 0,
                         0, 1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1)
        with pytest.raises(ValueError):
            rotation_matrix_to_quaternion(bad_mat)

    def test_result_is_unit_quaternion(self):
        """Результат rotation_matrix_to_quaternion завжди одиничний."""
        for angle_deg in [0, 30, 90, 180]:
            mat = Mat4x4.rotation_z(np.radians(angle_deg))
            q = rotation_matrix_to_quaternion(mat)
            assert is_unit_quaternion(q), f"Не одиничний кватерніон для {angle_deg}°"

    def test_quaternion_to_matrix_is_rotation_matrix(self):
        """quaternion_to_rotation_matrix дає ортогональну матрицю з det=1."""
        q = euler_to_quaternion(*np.radians((30, 45, 60)), "ZYX")
        mat = quaternion_to_rotation_matrix(q)
        r = mat.data[:3, :3]
        assert np.allclose(r @ r.T, np.eye(3), atol=1e-6)
        assert np.isclose(np.linalg.det(r), 1.0, atol=1e-6)


# ══════════════════════════════════════════════════════════════════════════════
# Кут-вісь ↔ Кватерніон
# ══════════════════════════════════════════════════════════════════════════════

class TestAngleAxisQuaternion:

    def test_angle_axis_to_quaternion_x(self):
        """angle_axis_to_quaternion для осі X = Quaternion.rotation_x."""
        angle = np.radians(60)
        q = angle_axis_to_quaternion(angle, [1, 0, 0])
        q_expected = Quaternion.rotation_x(angle)
        assert are_same_rotation(q, q_expected)

    def test_angle_axis_to_quaternion_y(self):
        """angle_axis_to_quaternion для осі Y = Quaternion.rotation_y."""
        angle = np.radians(90)
        q = angle_axis_to_quaternion(angle, [0, 1, 0])
        q_expected = Quaternion.rotation_y(angle)
        assert are_same_rotation(q, q_expected)

    def test_angle_axis_to_quaternion_z(self):
        """angle_axis_to_quaternion для осі Z = Quaternion.rotation_z."""
        angle = np.radians(45)
        q = angle_axis_to_quaternion(angle, [0, 0, 1])
        q_expected = Quaternion.rotation_z(angle)
        assert are_same_rotation(q, q_expected)

    def test_roundtrip_angle_axis(self):
        """angle_axis → quaternion → angle_axis дає вихідні значення."""
        angle_orig = np.radians(75)
        axis_orig = Vec3(1, 2, 3).normalized()
        q = angle_axis_to_quaternion(angle_orig, axis_orig)
        angle_rec, axis_rec = quaternion_to_angle_axis(q)
        assert np.isclose(angle_rec, angle_orig, atol=1e-6)
        assert np.allclose(axis_rec.data[:3], axis_orig.data[:3], atol=1e-6)

    def test_zero_angle_gives_identity(self):
        """Кут 0 → одиничний кватерніон незалежно від осі."""
        q = angle_axis_to_quaternion(0.0, [1, 0, 0])
        assert are_same_rotation(q, quaternion_identity())

    def test_rotation_consistency_with_matrix(self):
        """angle_axis кватерніон та матриця Mat4x4.rotation дають однакове обертання."""
        angle = np.radians(70)
        axis = [1, 1, 0]  # не нормалізована — обидва методи нормалізують
        q = angle_axis_to_quaternion(angle, axis)
        mat_from_q = quaternion_to_rotation_matrix(q)
        mat_direct = Mat4x4.rotation(angle, axis)
        assert np.allclose(mat_from_q.data, mat_direct.data, atol=1e-6)


# ══════════════════════════════════════════════════════════════════════════════
# SLERP
# ══════════════════════════════════════════════════════════════════════════════

class TestSlerp:

    def test_slerp_t0_gives_q0(self):
        """slerp(q0, q1, 0) = q0."""
        q0 = Quaternion.rotation_y(np.radians(30))
        q1 = Quaternion.rotation_y(np.radians(90))
        result = slerp(q0, q1, 0.0)
        assert are_same_rotation(result, q0)

    def test_slerp_t1_gives_q1(self):
        """slerp(q0, q1, 1) = q1."""
        q0 = Quaternion.rotation_y(np.radians(30))
        q1 = Quaternion.rotation_y(np.radians(90))
        result = slerp(q0, q1, 1.0)
        assert are_same_rotation(result, q1)

    def test_slerp_t05_midpoint(self):
        """slerp(q0, q1, 0.5) дає кватерніон посередині (кут = середньому)."""
        phi0, phi1 = np.radians(20), np.radians(80)
        q0 = Quaternion.rotation_y(phi0)
        q1 = Quaternion.rotation_y(phi1)
        q_mid = slerp(q0, q1, 0.5)
        q_expected = Quaternion.rotation_y((phi0 + phi1) / 2)
        assert are_same_rotation(q_mid, q_expected)

    def test_slerp_result_is_unit_quaternion(self):
        """slerp завжди повертає одиничний кватерніон."""
        q0 = euler_to_quaternion(*np.radians((10, 20, 30)), "XYZ")
        q1 = euler_to_quaternion(*np.radians((60, 45, 90)), "XYZ")
        for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
            q = slerp(q0, q1, t)
            assert is_unit_quaternion(q, atol=1e-6), f"slerp(t={t}) не є одиничним"

    def test_slerp_short_path(self):
        """slerp обирає короткий шлях між протилежними кватерніонами."""
        q0 = Quaternion.rotation_y(np.radians(10))
        q1_neg = -Quaternion.rotation_y(np.radians(20))  # той самий кватерніон, інший знак
        q1_pos = Quaternion.rotation_y(np.radians(20))
        angle_neg = angle_between_rotations(slerp(q0, q1_neg, 0.5), q0)
        angle_pos = angle_between_rotations(slerp(q0, q1_pos, 0.5), q0)
        assert np.isclose(angle_neg, angle_pos, atol=1e-5)

    def test_slerp_nearly_identical_quaternions(self):
        """slerp стабільний для майже однакових кватерніонів (dot ≈ 1)."""
        q0 = Quaternion.rotation_z(np.radians(45))
        q1 = Quaternion.rotation_z(np.radians(45.0001))
        result = slerp(q0, q1, 0.5)
        assert is_unit_quaternion(result, atol=1e-5)


# ══════════════════════════════════════════════════════════════════════════════
# NLERP
# ══════════════════════════════════════════════════════════════════════════════

class TestNlerp:

    def test_nlerp_t0_gives_q0(self):
        """nlerp(q0, q1, 0) = q0."""
        q0 = Quaternion.rotation_x(np.radians(30))
        q1 = Quaternion.rotation_x(np.radians(90))
        assert are_same_rotation(nlerp(q0, q1, 0.0), q0)

    def test_nlerp_t1_gives_q1(self):
        """nlerp(q0, q1, 1) = q1."""
        q0 = Quaternion.rotation_x(np.radians(30))
        q1 = Quaternion.rotation_x(np.radians(90))
        assert are_same_rotation(nlerp(q0, q1, 1.0), q1)

    def test_nlerp_result_is_unit_quaternion(self):
        """nlerp завжди повертає одиничний кватерніон."""
        q0 = euler_to_quaternion(*np.radians((10, 20, 30)), "ZYX")
        q1 = euler_to_quaternion(*np.radians((60, 45, 90)), "ZYX")
        for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
            q = nlerp(q0, q1, t)
            assert is_unit_quaternion(q, atol=1e-6), f"nlerp(t={t}) не є одиничним"

    def test_nlerp_short_path(self):
        """nlerp обирає короткий шлях між протилежними кватерніонами."""
        q0 = Quaternion.rotation_y(np.radians(10))
        q1_neg = -Quaternion.rotation_y(np.radians(20))
        q1_pos = Quaternion.rotation_y(np.radians(20))
        angle_neg = angle_between_rotations(nlerp(q0, q1_neg, 0.5), q0)
        angle_pos = angle_between_rotations(nlerp(q0, q1_pos, 0.5), q0)
        assert np.isclose(angle_neg, angle_pos, atol=1e-4)


# ══════════════════════════════════════════════════════════════════════════════
# Допоміжні функції
# ══════════════════════════════════════════════════════════════════════════════

class TestHelpers:

    def test_quaternion_dot_identical(self):
        """Скалярний добуток одиничного кватерніона сам з собою = 1."""
        q = euler_to_quaternion(*np.radians((30, 45, 60)), "XYZ")
        assert np.isclose(quaternion_dot(q, q), 1.0, atol=1e-6)

    def test_quaternion_dot_opposite(self):
        """Скалярний добуток q та -q = -1."""
        q = Quaternion.rotation_x(np.radians(45))
        assert np.isclose(quaternion_dot(q, -q), -1.0, atol=1e-6)

    def test_are_same_rotation_identical(self):
        """Однакові кватерніони → True."""
        q = Quaternion.rotation_y(np.radians(60))
        assert are_same_rotation(q, q)

    def test_are_same_rotation_negative(self):
        """q та -q → True (подвійне покриття SO(3))."""
        q = Quaternion.rotation_z(np.radians(45))
        assert are_same_rotation(q, -q)

    def test_are_same_rotation_different(self):
        """Різні обертання → False."""
        q0 = Quaternion.rotation_x(np.radians(30))
        q1 = Quaternion.rotation_x(np.radians(90))
        assert not are_same_rotation(q0, q1)

    def test_angle_between_rotations_same(self):
        """Кут між однаковими обертаннями = 0."""
        q = Quaternion.rotation_z(np.radians(45))
        assert np.isclose(angle_between_rotations(q, q), 0.0, atol=1e-6)

    def test_angle_between_rotations_90deg(self):
        """Кут між Ry(0°) та Ry(90°) = 90°."""
        q0 = quaternion_identity()
        q1 = Quaternion.rotation_y(np.radians(90))
        angle = angle_between_rotations(q0, q1)
        assert np.isclose(np.degrees(angle), 90.0, atol=1e-4)

    def test_angle_between_rotations_opposite_sign(self):
        """q та -q мають кут 0 між собою (одне й те саме обертання)."""
        q = Quaternion.rotation_x(np.radians(60))
        assert np.isclose(angle_between_rotations(q, -q), 0.0, atol=1e-6)

    def test_angle_between_rotations_symmetry(self):
        """angle_between_rotations симетрична."""
        q0 = Quaternion.rotation_y(np.radians(30))
        q1 = Quaternion.rotation_z(np.radians(60))
        assert np.isclose(
            angle_between_rotations(q0, q1),
            angle_between_rotations(q1, q0),
            atol=1e-6
        )

    def test_quaternion_identity_is_unit(self):
        """quaternion_identity() є одиничним."""
        assert is_unit_quaternion(quaternion_identity())

    def test_is_unit_quaternion_true(self):
        """Нормалізований кватерніон — одиничний."""
        q = Quaternion(1, 2, 3, 4).normalized()
        assert is_unit_quaternion(q)

    def test_is_unit_quaternion_false(self):
        """Ненормалізований кватерніон — не одиничний."""
        q = Quaternion(1, 2, 3, 4)  # норма > 1
        assert not is_unit_quaternion(q)

    def test_quaternion_identity_no_rotation(self):
        """quaternion_identity() → нульовий кут обертання."""
        angle, _ = quaternion_to_angle_axis(quaternion_identity())
        assert np.isclose(angle, 0.0, atol=1e-6)


# ══════════════════════════════════════════════════════════════════════════════
# Інтеграційні тести (euler → quaternion → matrix узгоджені)
# ══════════════════════════════════════════════════════════════════════════════

class TestIntegration:

    def test_euler_quat_matrix_consistency(self):
        """Матриці обертання, отримані через кватерніон та напряму, збігаються."""
        angles = np.radians((30, 45, 60))
        for cfg in ALL_CONFIGS:
            mat_direct = Mat4x4.rotation_euler(*angles, configuration=cfg)
            q = euler_to_quaternion(*angles, cfg)
            mat_via_quat = quaternion_to_rotation_matrix(q)
            assert np.allclose(mat_direct.data, mat_via_quat.data, atol=1e-6), \
                f"{cfg}: матриці через кватерніон та напряму відрізняються"

    def test_rotate_vector_quaternion_vs_matrix(self):
        """Поворот вектора через кватерніон та матрицю дає однаковий результат."""
        phi, theta, psi = np.radians((30, 45, 60))
        q = euler_xyz_to_quaternion(phi, theta, psi)
        mat = Mat4x4.rotation_euler(phi, theta, psi, "XYZ")

        from src.math.Vec3 import Vec3
        v = Vec3(1, 2, 3)
        v_quat = q.rotate_vector(v)
        v_mat = mat @ v
        assert np.allclose(v_quat.data[:3], v_mat.data[:3], atol=1e-6)

    def test_composition_euler_via_quaternions(self):
        """Послідовне застосування двох обертань через кватерніони = матриця добутку."""
        phi, theta = np.radians(45), np.radians(30)
        q1 = Quaternion.rotation_x(phi)
        q2 = Quaternion.rotation_y(theta)
        q_composed = q1 * q2

        mat1 = Mat4x4.rotation_x(phi)
        mat2 = Mat4x4.rotation_y(theta)
        mat_composed = mat1 * mat2

        mat_from_q = quaternion_to_rotation_matrix(q_composed)
        assert np.allclose(mat_from_q.data, mat_composed.data, atol=1e-6)

    def test_slerp_endpoints_match_euler(self):
        """SLERP кінцеві точки відповідають кватерніонам, побудованим з кутів Ейлера."""
        q0 = euler_to_quaternion(*np.radians((10, 20, 30)), "ZYX")
        q1 = euler_to_quaternion(*np.radians((60, 45, 90)), "ZYX")
        assert are_same_rotation(slerp(q0, q1, 0.0), q0)
        assert are_same_rotation(slerp(q0, q1, 1.0), q1)
