import numpy as np

from src.math.Mat3x3 import Mat3x3
from src.math.Rotations import rotation_matrix_z, rotation_matrix_x, rotation_matrix_y
from src.math.Scale import scale_matrix
from src.math.Translation import translation_matrix
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4


class Mat4x4:
    ERROR_MESSAGE_CONSTRUCTOR = "Непідтриманий тип даних для ініціалізації або недостатньо елементів для побудови матриці 4x4."
    ERROR_MESSAGE_ADD = "Додавання можливе лише з іншими об'єктами Matrix4x4 або numpy.ndarray 4x4."
    ERROR_MESSAGE_MULT = "Множення можливе лише з іншими об'єктами Matrix4x4 або numpy.ndarray 4x4."
    ERROR_MESSAGE_INV_DOESNT_EXIST = "Матриця не має оберненої."
    ERROR_MESSAGE_ROTATION = "Вектор повороту повинен містити рівно 3 дійсних елементи."
    ERROR_MESSAGE_SCALE = "Недостатньо даних, щоб сформувати матрицю розтягу"
    ERROR_MESSAGE_EULER_CONFIG_UNKNOWN = "Unknown Euler configuration"

    # Tait-Bryan конфігурації (всі осі різні)
    XYZ = "XYZ"
    XZY = "XZY"
    YXZ = "YXZ"
    YZX = "YZX"
    ZXY = "ZXY"
    ZYX = "ZYX"

    # Власні кути Ейлера (перша та третя вісь однакові)
    XYX = "XYX"
    XZX = "XZX"
    YXY = "YXY"
    YZY = "YZY"
    ZXZ = "ZXZ"
    ZYZ = "ZYZ"

    def __init__(self, *data):
        """
        Конструктор класу Matrix3x3.
        Якщо дані не передані, створює одиничну матрицю.
        Приймає:
        - 3x3 матрицю (numpy.ndarray),
        - список списків 2x2 або 3x3,
        - інший об'єкт Matrix3x3.
        """
        if len(data) == 0:
            # Якщо дані не передані, створюємо одиничну матрицю
            self.data = np.eye(4, dtype=float)
        elif len(data) == 16:
            elements = np.array(data, dtype=float)
            self.data = elements.reshape((4, 4))
        elif len(data) == 9:
            elements = np.array(data, dtype=float)
            elements = elements.reshape((3, 3))
            self.data = np.eye(4, dtype=float)
            self.data[:3, :3] = elements
        elif len(data) == 4:
            if all(isinstance(vec, Vec4) for vec in data):
                self.data = np.vstack([vec.data for vec in data])
            elif all(isinstance(vec, (np.ndarray, tuple, list)) for vec in data):
                self.data = np.vstack([vec for vec in data])
            elif all(isinstance(el, (float, int)) for el in data):
                elements = np.array(data, dtype=float)
                elements = elements.reshape((2, 2))
                self.data = np.eye(4, dtype=float)
                self.data[:2, :2] = elements
        elif len(data) == 1:
            data = data[0]
            if isinstance(data, Mat4x4):
                # Якщо переданий об'єкт Matrix4x4
                self.data = np.copy(data.data)
            elif isinstance(data, Mat3x3):
                # Якщо переданий об'єкт Matrix3x3
                self.data = np.eye(4, dtype=float)
                self.data[:3, :3] = data.data
            elif isinstance(data, (list, tuple, np.ndarray)):
                try:
                    data = np.array(data)
                    if data.shape == (4, 4):
                        # Якщо передана 4x4 матриця
                        self.data = np.array(data, dtype=float)
                    elif data.shape == (3, 3):
                        # Якщо передана 3x3 матриця, доповнюємо до 4x4
                        self.data = np.eye(4, dtype=float)
                        self.data[:3, :3] = data
                    elif data.shape == (2, 2):
                        # Якщо передана 2x2 матриця, доповнюємо до 4x4
                        self.data = np.eye(4, dtype=float)
                        self.data[:2, :2] = data
                    else:
                        raise ValueError(Mat4x4.ERROR_MESSAGE_CONSTRUCTOR)
                except ValueError:
                    raise ValueError(Mat4x4.ERROR_MESSAGE_CONSTRUCTOR)

            else:
                raise ValueError(Mat4x4.ERROR_MESSAGE_CONSTRUCTOR)
        else:
            raise ValueError(Mat4x4.ERROR_MESSAGE_CONSTRUCTOR)

    def __getitem__(self, indices):
        """
        Отримання елемента матриці по індексах (рядок, стовпчик).
        """
        row, col = indices
        return self.data[row, col]

    def __setitem__(self, indices, value):
        """
        Встановлення значення елемента матриці по індексах (рядок, стовпчик).
        """
        row, col = indices
        self.data[row, col] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Повертає строкове представлення матриці.
        """
        return np.array2string(self.data, formatter={'float_kind': lambda x: f"{x:8.3f}"})

    def __matmul__(self, other):
        """
        Реалізує множення матриці на іншу Matrix3x3, numpy.ndarray 3x3, або Vector3.
        """
        if not isinstance(other, (Mat4x4, np.ndarray, Vec3, Vec4)):
            raise TypeError(Mat4x4.ERROR_MESSAGE_MULT)

        if isinstance(other, np.ndarray):
            if other.shape == (4,4):
                return self @ Mat4x4(other)
            elif other.shape == (4,):
                return self @ Vec4(other)
            else:
                raise TypeError(Mat4x4.ERROR_MESSAGE_MULT)
        elif isinstance(other, Mat4x4):
            return Mat4x4(np.dot(self.data, other.data))
        elif isinstance(other, Vec4):
            return Vec4(np.dot(self.data, other.data))
        elif isinstance(other, Vec3):
            return self @ Vec4(other)
        return Mat4x4(np.dot(self.data, other))

    def __add__(self, other):
        """
        Реалізує додавання двох матриць Matrix3x3 або numpy.ndarray 3x3.
        """
        if not isinstance(other, (Mat4x4, np.ndarray)):
            raise TypeError(Mat4x4.ERROR_MESSAGE_ADD)
        if isinstance(other, Mat4x4):
            return Mat4x4(self.data + other.data)
        return Mat4x4(self.data + other)

    def __sub__(self, other):
        if not isinstance(other, (Mat4x4, np.ndarray)):
            raise TypeError(Mat4x4.ERROR_MESSAGE_ADD)
        if isinstance(other, Mat4x4):
            return Mat4x4(self.data - other.data)
        return Mat4x4(self.data - other)

    def __neg__(self):
        return Mat4x4(-self.data)

    def __mul__(self, other):
        """
        Реалізує множення матриці на іншу Matrix3x3, numpy.ndarray 3x3, або Vector3.
        """
        return self.__matmul__(other)

    def inverse(self):
        """
        Обчислює обернену матрицю.
        """
        det = np.linalg.det(self.data)
        if np.isclose(det, 0):
            raise ValueError(Mat4x4.ERROR_MESSAGE_INV_DOESNT_EXIST)
        return Mat4x4(np.linalg.inv(self.data))

    def norm(self):
        return np.linalg.norm(self.data)

    @staticmethod
    def identity():
        return Mat4x4()

    @property
    def T(self):
        return Mat4x4(self.data.T)

    def transpose(self):
        return Mat4x4(self.data.transpose())

    @staticmethod
    def rotation_x(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)
        m = rotation_matrix_x(angle)
        return Mat4x4(m)

    @staticmethod
    def rotation_y(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)
        m = rotation_matrix_y(angle)
        return Mat4x4(m)

    @staticmethod
    def rotation_z(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)

        m = rotation_matrix_z(angle)
        return Mat4x4(m)

    @staticmethod
    def rotation(angle, axis, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)

        if isinstance(axis, (Vec3, Vec4)):
            axis = axis.xyz
        elif isinstance(axis, (np.ndarray, tuple, list,)):
            axis = np.array(axis)
            if axis.shape == (3,):
                axis = axis.astype(float)
            else:
                raise ValueError(Mat4x4.ERROR_MESSAGE_ROTATION)

        norm = np.linalg.norm(axis)

        # Нормалізований вектор
        if norm != 0:
            normalized_v = axis.data / norm
        else:
            normalized_v = axis  # Для нульового вектора нормалізація не визначена

        ux, uy, uz = normalized_v

        phy = np.arctan2(ux, uz)
        # print(np.degrees(phy))
        len_ux_uz = np.linalg.norm((ux, uz))
        theta = np.arctan2(uy, len_ux_uz)
        # print(np.degrees(theta))

        Ry = Mat4x4.rotation_y(-phy)
        Rx = Mat4x4.rotation_x(theta)
        Rz = Mat4x4.rotation_z(angle)

        Ry_1 = Ry.inverse()
        Rx_1 = Rx.inverse()

        return Ry_1 * Rx_1 * Rz * Rx * Ry

    @staticmethod
    def rotation_euler(phi, theta, psi, configuration=XYZ):
        """
        Формує матрицю обертання для заданих кутів Ейлера (phi, theta, psi)
        та конфігурації осей обертання.

        Підтримувані конфігурації Tait-Bryan (всі осі різні):
            XYZ, XZY, YXZ, YZX, ZXY, ZYX
        Підтримувані власні кути Ейлера (перша та третя вісь однакові):
            XYX, XZX, YXY, YZY, ZXZ, ZYZ
        """
        Rx = Mat4x4.rotation_x
        Ry = Mat4x4.rotation_y
        Rz = Mat4x4.rotation_z
        configuration = configuration.upper()
        # --- Tait-Bryan ---
        if configuration == Mat4x4.XYZ:
            return Rx(phi) * Ry(theta) * Rz(psi)
        elif configuration == Mat4x4.XZY:
            return Rx(phi) * Rz(theta) * Ry(psi)
        elif configuration == Mat4x4.YXZ:
            return Ry(phi) * Rx(theta) * Rz(psi)
        elif configuration == Mat4x4.YZX:
            return Ry(phi) * Rz(theta) * Rx(psi)
        elif configuration == Mat4x4.ZXY:
            return Rz(phi) * Rx(theta) * Ry(psi)
        elif configuration == Mat4x4.ZYX:
            return Rz(phi) * Ry(theta) * Rx(psi)
        # --- Власні кути Ейлера ---
        elif configuration == Mat4x4.XYX:
            return Rx(phi) * Ry(theta) * Rx(psi)
        elif configuration == Mat4x4.XZX:
            return Rx(phi) * Rz(theta) * Rx(psi)
        elif configuration == Mat4x4.YXY:
            return Ry(phi) * Rx(theta) * Ry(psi)
        elif configuration == Mat4x4.YZY:
            return Ry(phi) * Rz(theta) * Ry(psi)
        elif configuration == Mat4x4.ZXZ:
            return Rz(phi) * Rx(theta) * Rz(psi)
        elif configuration == Mat4x4.ZYZ:
            return Rz(phi) * Ry(theta) * Rz(psi)
        else:
            raise ValueError(Mat4x4.ERROR_MESSAGE_EULER_CONFIG_UNKNOWN)

    def toEuler(self, configuration=XYZ):
        """
        Декомпозує матрицю обертання у кути Ейлера (phi, theta, psi)
        для заданої конфігурації.

        Повертає кортеж (phi, theta, psi) у радіанах.
        """
        configuration = configuration.upper()
        # --- Tait-Bryan ---
        if configuration == Mat4x4.XYZ:
            return Mat4x4.toEulerXYZ(self)
        elif configuration == Mat4x4.XZY:
            return Mat4x4.toEulerXZY(self)
        elif configuration == Mat4x4.YXZ:
            return Mat4x4.toEulerYXZ(self)
        elif configuration == Mat4x4.YZX:
            return Mat4x4.toEulerYZX(self)
        elif configuration == Mat4x4.ZXY:
            return Mat4x4.toEulerZXY(self)
        elif configuration == Mat4x4.ZYX:
            return Mat4x4.toEulerZYX(self)
        # --- Власні кути Ейлера ---
        elif configuration == Mat4x4.XYX:
            return Mat4x4.toEulerXYX(self)
        elif configuration == Mat4x4.XZX:
            return Mat4x4.toEulerXZX(self)
        elif configuration == Mat4x4.YXY:
            return Mat4x4.toEulerYXY(self)
        elif configuration == Mat4x4.YZY:
            return Mat4x4.toEulerYZY(self)
        elif configuration == Mat4x4.ZXZ:
            return Mat4x4.toEulerZXZ(self)
        elif configuration == Mat4x4.ZYZ:
            return Mat4x4.toEulerZYZ(self)
        else:
            raise ValueError(Mat4x4.ERROR_MESSAGE_EULER_CONFIG_UNKNOWN)

    # ── Tait-Bryan: декомпозиції ──────────────────────────────────────────────

    @staticmethod
    def toEulerXYZ(r):
        """R = Rx(phi) * Ry(theta) * Rz(psi)"""
        phi   = np.arctan2(-r[1, 2], r[2, 2])
        theta = np.arcsin( r[0, 2])
        psi   = np.arctan2(-r[0, 1], r[0, 0])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerXZY(r):
        """R = Rx(phi) * Rz(theta) * Ry(psi)"""
        phi   = np.arctan2( r[2, 1], r[1, 1])
        theta = np.arcsin(-r[0, 1])
        psi   = np.arctan2( r[0, 2], r[0, 0])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerYXZ(r):
        """R = Ry(phi) * Rx(theta) * Rz(psi)"""
        phi   = np.arctan2( r[0, 2], r[2, 2])
        theta = np.arcsin(-r[1, 2])
        psi   = np.arctan2( r[1, 0], r[1, 1])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerYZX(r):
        """R = Ry(phi) * Rz(theta) * Rx(psi)"""
        phi   = np.arctan2(-r[2, 0], r[0, 0])
        theta = np.arcsin( r[1, 0])
        psi   = np.arctan2(-r[1, 2], r[1, 1])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerZXY(r):
        """R = Rz(phi) * Rx(theta) * Ry(psi)"""
        phi   = np.arctan2(-r[0, 1], r[1, 1])
        theta = np.arcsin( r[2, 1])
        psi   = np.arctan2(-r[2, 0], r[2, 2])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerZYX(r):
        """R = Rz(phi) * Ry(theta) * Rx(psi)"""
        phi   = np.arctan2( r[1, 0], r[0, 0])
        theta = np.arcsin(-r[2, 0])
        psi   = np.arctan2( r[2, 1], r[2, 2])
        return float(phi), float(theta), float(psi)

    # ── Власні кути Ейлера: декомпозиції ─────────────────────────────────────

    @staticmethod
    def toEulerZXZ(r):
        """R = Rz(phi) * Rx(theta) * Rz(psi)"""
        phi   = np.arctan2( r[0, 2], -r[1, 2])
        theta = np.arccos(  r[2, 2])
        psi   = np.arctan2( r[2, 0],  r[2, 1])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerZYZ(r):
        """R = Rz(phi) * Ry(theta) * Rz(psi)"""
        phi   = np.arctan2( r[1, 2],  r[0, 2])
        theta = np.arccos(  r[2, 2])
        psi   = np.arctan2( r[2, 1], -r[2, 0])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerXYX(r):
        """R = Rx(phi) * Ry(theta) * Rx(psi)"""
        phi   = np.arctan2( r[1, 0], -r[2, 0])
        theta = np.arccos(  r[0, 0])
        psi   = np.arctan2( r[0, 1],  r[0, 2])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerXZX(r):
        """R = Rx(phi) * Rz(theta) * Rx(psi)"""
        phi   = np.arctan2( r[2, 0],  r[1, 0])
        theta = np.arccos(  r[0, 0])
        psi   = np.arctan2( r[0, 2], -r[0, 1])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerYXY(r):
        """R = Ry(phi) * Rx(theta) * Ry(psi)"""
        phi   = np.arctan2( r[0, 1],  r[2, 1])
        theta = np.arccos(  r[1, 1])
        psi   = np.arctan2( r[1, 0], -r[1, 2])
        return float(phi), float(theta), float(psi)

    @staticmethod
    def toEulerYZY(r):
        """R = Ry(phi) * Rz(theta) * Ry(psi)"""
        phi   = np.arctan2( r[2, 1], -r[0, 1])
        theta = np.arccos(  r[1, 1])
        psi   = np.arctan2( r[1, 2],  r[1, 0])
        return float(phi), float(theta), float(psi)

    def to_angle_axis(self):
        return Mat3x3.rotation_matrix_to_angle_axis(self)

    @staticmethod
    def translation(tx, ty=None, tz=None):
        if ty is None and isinstance(tx, (Vec3, Vec4)):
            m = translation_matrix(*tx.xyz)
        elif ty is None and isinstance(tx, np.ndarray):
            m = translation_matrix(tx[0], tx[1], tx[2])
        else:
            m = translation_matrix(tx, ty, tz)
        return Mat4x4(m)

    @staticmethod
    def scale(sx, sy=None, sz=None):
        if sy is None and isinstance(sx, (int, float)):
            m = scale_matrix(sx, sx, sx)
        elif sy is None and isinstance(sx, (Vec4, Vec3)):
            m = scale_matrix(*sx.xyz)
        elif sy is None and isinstance(sx, np.ndarray) and len(sx) == 3:
            m = scale_matrix(sx[0], sx[1], sx[2])
        elif isinstance(sx, (int, float)) and isinstance(sy, (int, float)) and isinstance(sz, (int, float)):
            m = scale_matrix(sx, sy, sz)
        else:
            raise ValueError(Mat4x4.ERROR_MESSAGE_SCALE)
        return Mat4x4(m)


# Приклад використання
if __name__ == "__main__":
    m = Mat4x4(1, 2, 3, 4,
                 5, 6, 7, 8,
                 9, 10, 11, 12,
                 13, 14, 15, 16
                 )
    v = Vec4(1, 2, 3)
    MV =  m * v
    print(MV)

    M = Mat4x4.rotation_euler(
        np.radians(30),
        np.radians(45),
        np.radians(15),
    )


