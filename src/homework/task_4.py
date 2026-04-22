import numpy as np
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Cube import Cube
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import vertex

if __name__ == '__main__':
    CUBE_KEY = "cube"
    CUBE_TARGET_KEY = "cube_target"

    az, ay, ax = np.radians(20), np.radians(35), np.radians(50)
    translation_vector = Vec3(1, 3, -2)

    R = Mat4x4.rotation_euler(az, ay, ax, configuration=Mat4x4.ZYX)
    T = Mat4x4.translation(translation_vector)
    M_final = T * R

    class CubeScene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"] = (-2, -1, -4, 4, 6, 3)
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

    animated_scene = CubeScene(title="Task 4: Euler ZYX Rotation -> Translation")
    frames_num = 60

    animated_scene.add_animation(TrsTransformationAnimation(end=R, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(TranslationAnimation(end=translation_vector, frames=frames_num, channel=CUBE_KEY))

    animated_scene.show()