import numpy as np
from src.engine.model.Cube import Cube
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import vertex

if __name__ == '__main__':
    a30, a45, a60 = np.radians(30), np.radians(45), np.radians(60)

    Rx = Mat4x4.rotation_x(a30)
    Ry = Mat4x4.rotation_y(a45)
    Rz = Mat4x4.rotation_z(a60)

    Ma = Rz * Ry * Rx
    Mb = Rz * Ry * Rx

    print("--- Матриці трансформації ---")
    print("Матриця А:\n", np.round(Ma.data, 4))
    print("\nМатриця Б:\n", np.round(Mb.data, 4))
    print(f"\nІдентичність: {np.allclose(Ma.data, Mb.data)}")
