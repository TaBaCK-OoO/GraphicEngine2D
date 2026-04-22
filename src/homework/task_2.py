import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4

if __name__ == '__main__':
    CUBE_KEY = "cube"
    CUBE_TARGET_KEY = "cube_target"

    scales = Vec3(2.0, 0.5, 1.0)
    angle_x, angle_y, angle_z = np.radians(30), np.radians(45), np.radians(60)
    OX, OY, OZ = Vec4(1, 0, 0), Vec4(0, 1, 0), Vec4(0, 0, 1)
    translation_vector = Vec3(-3, 2, 5)

    S = Mat4x4.scale(scales)
    Rx = Mat4x4.rotation_x(angle_x, is_radians=True)
    Ry = Mat4x4.rotation_y(angle_y, is_radians=True)
    Rz = Mat4x4.rotation_z(angle_z, is_radians=True)
    T = Mat4x4.translation(translation_vector)
    M_final = T * (Rz * Ry * Rx) * S

    class CubeScene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"] = (-4, -2, -2, 5, 5, 7)
            super().__init__(**kwargs)

            cube = Cube(alpha=0.1)
            self[CUBE_KEY] = cube
            cube.show_local_frame()

            cube_target = Cube(alpha=0.1, color="grey", line_width=0.5, line_style="-.")
            cube_target.transformation = M_final
            self[CUBE_TARGET_KEY] = cube_target
            cube_target.show_local_frame()

    animated_scene = CubeScene(title="Task 2: Scale -> Euler XYZ -> Translation")
    frames_num = 60

    animated_scene.add_animation(ScaleAnimation(end=scales, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(RotationAnimation(end=angle_x, axis=OX, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(RotationAnimation(end=angle_y, axis=OY, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(RotationAnimation(end=angle_z, axis=OZ, frames=frames_num, channel=CUBE_KEY))
    animated_scene.add_animation(TranslationAnimation(end=translation_vector, frames=frames_num, channel=CUBE_KEY))

    animated_scene.show()