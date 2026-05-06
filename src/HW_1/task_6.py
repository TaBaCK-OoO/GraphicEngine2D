import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Cube import Cube
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    CUBE_KEY = "cube"
    TARGET_KEY = "target"

    pivot_point = Vec3(2, 0, 3)
    rotation_axis = Vec4(0, 1, 0)
    angle_rad = np.radians(45)
    translation_vector = Vec3(-1, 2, 4)

    T_to_origin = Mat4x4.translation(-pivot_point)
    R = Mat4x4.rotation(angle_rad, rotation_axis, is_radians=True)
    T_back = Mat4x4.translation(pivot_point)

    M1_pivot_rotation = T_back * R * T_to_origin
    M2_translation = Mat4x4.translation(translation_vector)
    M_final = M2_translation * M1_pivot_rotation

    class PivotScene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"] = (-3, -1, -1, 6, 6, 9)
            kwargs["axis_show"] = False
            super().__init__(**kwargs)

            O = vertex(0, 0, 0)
            self["axis_x"] = Vector(O, vertex(5, 0, 0), color="red")
            self["axis_y"] = Vector(O, vertex(0, 5, 0), color="green")
            self["axis_z"] = Vector(O, vertex(0, 0, 5), color="blue")
            self["pivot_marker"] = Vector(O, vertex(*pivot_point.xyz), color="orange")

            cube = Cube(color="cyan", alpha=0.5)
            cube.show_local_frame()
            self[CUBE_KEY] = cube

            target = Cube(color="grey", alpha=0.2, edge_color="grey", line_style="--")
            target.transformation = M_final
            self[TARGET_KEY] = target

    scene = PivotScene(title="Task 6: Pivot Rotation (2,0,3) -> Translation")
    scene[CUBE_KEY].pivot(*pivot_point.xyz)
    scene[CUBE_KEY].show_pivot(True)

    frames = 60
    scene.add_animation(RotationAnimation(end=angle_rad, axis=rotation_axis, frames=frames, channel=CUBE_KEY))
    scene.add_animation(TranslationAnimation(end=translation_vector, frames=frames, channel=CUBE_KEY))

    scene.show()