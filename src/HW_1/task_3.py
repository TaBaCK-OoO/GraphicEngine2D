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
    CUBE_TARGET_KEY = "cube_target"

    angle_1 = np.radians(60)
    axis_1 = Vec4(0, 0, 1)
    angle_2 = np.radians(45)
    axis_2 = Vec4(1, 1, 1).normalized()
    translation_vector = Vec3(4, -2, 1)

    R1 = Mat4x4.rotation_z(angle_1, is_radians=True)
    R2 = Mat4x4.rotation(angle_2, axis_2, is_radians=True)
    T = Mat4x4.translation(translation_vector)
    M_final = T * R2 * R1

    class CubeScene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"] = (-1, -4, -1, 6, 3, 4)
            kwargs["axis_show"] = False
            super().__init__(**kwargs)

            O = vertex(0, 0, 0)
            self["axis_x"] = Vector(O, vertex(5, 0, 0), color="red")
            self["axis_y"] = Vector(O, vertex(0, 5, 0), color="green")
            self["axis_z"] = Vector(O, vertex(0, 0, 5), color="blue")

            cube = Cube(alpha=0.1)
            self[CUBE_KEY] = cube
            cube.show_local_frame()

            cube_target = Cube(alpha=0.1, color="grey", line_width=0.5, line_style="-.")
            cube_target.transformation = M_final
            self[CUBE_TARGET_KEY] = cube_target
            cube_target.show_local_frame()

    animated_scene = CubeScene(title="Task 3: Z-Rotation -> Arbitrary Axis Rotation -> Translation")
    frames_num = 60

    animated_scene.add_animation(RotationAnimation(end=angle_1, axis=axis_1, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(RotationAnimation(end=angle_2, axis=axis_2, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(TranslationAnimation(end=translation_vector, frames=frames_num, channel=CUBE_KEY))

    animated_scene.show()