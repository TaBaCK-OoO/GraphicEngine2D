import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Cube import Cube
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    CUBE_KEY, TARGET_KEY = "cube", "target"
    pivot = Vec3(1, 1, 1)
    scale_f = Vec3(2, 1, 1)
    ay, ax_y = np.radians(45), Vec4(0, 1, 0)
    tv = Vec3(-3, 4, 2)

    T_to, T_back = Mat4x4.translation(-pivot), Mat4x4.translation(pivot)
    Ms_p = T_back * Mat4x4.scale(scale_f) * T_to
    Mr_p = T_back * Mat4x4.rotation_y(ay) * T_to
    M_final = Mat4x4.translation(tv) * Mr_p * Ms_p


    class Task10Scene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"], kwargs["axis_show"] = (-5, -2, -2, 4, 7, 6), False
            super().__init__(**kwargs)
            O = vertex(0, 0, 0)
            self["x"], self["y"], self["z"] = Vector(O, vertex(5, 0, 0), color="red"), Vector(O, vertex(0, 5, 0),
                                                                                              color="green"), Vector(O,
                                                                                                                     vertex(
                                                                                                                         0,
                                                                                                                         0,
                                                                                                                         5),
                                                                                                                     color="blue")
            self["p"] = Vector(O, vertex(*pivot.xyz), color="orange")

            c = Cube(color="cyan", alpha=0.3)
            c.show_pivot(True)
            self[CUBE_KEY] = c

            t = Cube(color="grey", alpha=0.1, edge_color="grey", line_style="-.")
            t.transformation = M_final
            self[TARGET_KEY] = t


    scene = Task10Scene(title="Завдання 10: Комплексна трансформація навколо P(1,1,1)")
    scene[CUBE_KEY].pivot(*pivot.xyz)

    f = 60
    scene.add_animation(ScaleAnimation(end=scale_f, frames=f, channel=CUBE_KEY))
    scene.add_animation(RotationAnimation(end=ay, axis=ax_y, frames=f, channel=CUBE_KEY))
    scene.add_animation(TranslationAnimation(end=tv, frames=f, channel=CUBE_KEY))
    scene.show()