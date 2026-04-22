import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.model.Cube import Cube
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    CUBE_KEY, TARGET_KEY = "cube", "target"

    pivot = Vec3(1, 2, 3)
    scale_factors = Vec3(1, 1, 3)
    angle_rad = np.radians(30)
    rot_axis = Vec4(0, 0, 1)

    T_minus = Mat4x4.translation(-pivot)
    S = Mat4x4.scale(scale_factors)
    R = Mat4x4.rotation_z(angle_rad)
    T_plus = Mat4x4.translation(pivot)

    # Результуюча матриця (Scale -> Rotate навколо Pivot)
    M_final = T_plus * R * S * T_minus


    class PivotComplexScene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"], kwargs["axis_show"] = (-2, -1, -7, 5, 5, 5), False
            super().__init__(**kwargs)
            O = vertex(0, 0, 0)
            self["ax"] = Vector(O, vertex(5, 0, 0), color="red")
            self["ay"] = Vector(O, vertex(0, 5, 0), color="green")
            self["az"] = Vector(O, vertex(0, 0, 5), color="blue")
            self["p"] = Vector(O, vertex(*pivot.xyz), color="orange")

            c = Cube(color="cyan", alpha=0.4)
            c.show_local_frame()
            self[CUBE_KEY] = c

            t = Cube(color="grey", alpha=0.1, edge_color="grey", line_style="--")
            t.transformation = M_final
            self[TARGET_KEY] = t


    scene = PivotComplexScene(title="Task 7: Scale & Rotate around P(1,2,3)")
    scene[CUBE_KEY].pivot(*pivot.xyz)
    scene[CUBE_KEY].show_pivot(True)

    f = 60
    scene.add_animation(ScaleAnimation(end=scale_factors, frames=f, channel=CUBE_KEY))
    scene.add_animation(RotationAnimation(end=angle_rad, axis=rot_axis, frames=f, channel=CUBE_KEY))
    scene.show()