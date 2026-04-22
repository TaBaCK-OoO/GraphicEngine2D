import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    RECT_KEY, TARGET_KEY = "rect", "target"

    v0, v1, v2, v3 = vertex(1, 2, 0), vertex(4, 2, 0), vertex(4, 5, 0), vertex(1, 5, 0)
    pivot_point = Vec3(3, 3, 0)
    ay, ax = np.radians(60), np.radians(30)

    T_to = Mat4x4.translation(-pivot_point)
    T_back = Mat4x4.translation(pivot_point)

    My = T_back * Mat4x4.rotation_y(ay) * T_to
    Mx = T_back * Mat4x4.rotation_x(ax) * T_to
    M_final = Mx * My


    class Task9Scene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"], kwargs["axis_show"] = (0, 0, -3, 6, 6, 4), False
            super().__init__(**kwargs)
            O = vertex(0, 0, 0)
            self["x"], self["y"], self["z"] = Vector(O, vertex(6, 0, 0), color="red"), Vector(O, vertex(0, 6, 0),
                                                                                              color="green"), Vector(O,
                                                                                                                     vertex(
                                                                                                                         0,
                                                                                                                         0,
                                                                                                                         6),
                                                                                                                     color="blue")

            rect = SimplePolygon(v0, v1, v2, v3, color="blue", alpha=0.4)
            rect.show_pivot(True)
            self[RECT_KEY] = rect

            target = SimplePolygon(v0, v1, v2, v3, color="grey", alpha=0.1, line_style="-.")
            target.transformation = M_final
            self[TARGET_KEY] = target


    scene = Task9Scene(title="Завдання 9: Perspective Shift (Euler Pivot)")
    scene[RECT_KEY].pivot(pivot_point.x, pivot_point.y, pivot_point.z)

    f = 60
    scene.add_animation(RotationAnimation(end=ay, axis=Vec4(0, 1, 0), frames=f, channel=RECT_KEY))
    scene.add_animation(RotationAnimation(end=ax, axis=Vec4(1, 0, 0), frames=f, channel=RECT_KEY))
    scene.show()