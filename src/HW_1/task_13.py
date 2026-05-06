import numpy as np
from src.engine.model.Tetrahedron import Tetrahedron
from src.math.Mat4x4 import Mat4x4

if __name__ == '__main__':
    tetra = Tetrahedron()

    rx45 = Mat4x4.rotation_x(np.radians(45))
    tz2 = Mat4x4.translation(0, 0, 2)
    ry30 = Mat4x4.rotation_y(np.radians(30))

    m1 = rx45
    m2 = m1 * tz2
    m3 = m2 * ry30

    steps = [m1, m2, m3]
    labels = ["Step 1: Rot X (45°)", "Step 2: Local Trans Z (2)", "Step 3: Local Rot Y (30°)"]

    print("--- Task 13 Final World Coordinates ---")
    for label, m in zip(labels, steps):
        print(f"\n{label}:")
        for i, v in enumerate(tetra._geometry):
            v_world = m * v
            print(f"  V{i}: {np.round(v_world.xyz, 3)}")