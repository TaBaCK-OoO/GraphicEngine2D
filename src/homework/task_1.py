import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4

if __name__ == '__main__':
    CUBE_KEY = "cube"
    CUBE_TARGET_KEY = "cube_target"

    axis = Vec4(1, 1, 0).normalized()
    angle = np.radians(45)
    translation_vector = Vec3(2, -1, 3)

    R = Mat4x4.rotation(angle, axis)
    T = Mat4x4.translation(translation_vector)
    M_final = T * R

    class CubeScene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"] = (-2, -3, -2, 6, 6, 6)
            super().__init__(**kwargs)

            cube = Cube(alpha=0.1)
            self[CUBE_KEY] = cube
            cube.show_local_frame()

            cube_target = Cube(alpha=0.1, color="grey", line_width=0.5, line_style="-.")
            cube_target.transformation = M_final
            self[CUBE_TARGET_KEY] = cube_target
            cube_target.show_local_frame()

    animated_scene = CubeScene(title="Task 1: Transform Composition")
    frames_num = 60

    anim_rot = RotationAnimation(
        end=angle,
        axis=axis,
        frames=frames_num,
        channel=CUBE_KEY
    )

    anim_trans = TranslationAnimation(
        end=translation_vector,
        frames=frames_num,
        channel=CUBE_KEY
    )

    animated_scene.add_animation(anim_rot)
    animated_scene.add_animation(anim_trans)

    animated_scene.show()