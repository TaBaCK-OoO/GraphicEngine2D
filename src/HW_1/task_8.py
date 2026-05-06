import numpy as np
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import vertex

if __name__ == '__main__':
    TRI_KEY, TARGET_KEY = "triangle", "target"

    v0, v1, v2 = vertex(1, 2, 3), vertex(4, 10, 6), vertex(7, 8, 9)
    pivot_point = Vec3(2, 3, 4)
    axis = vertex(1, 1, 1).normalized()
    angle = np.radians(90)
    translation_vector = Vec3(0, -3, 2)

    T_to_origin = Mat4x4.translation(-pivot_point)
    R = Mat4x4.rotation(angle, axis)
    T_back = Mat4x4.translation(pivot_point)
    M_pivot_rot = T_back * R * T_to_origin
    M_final = Mat4x4.translation(translation_vector) * M_pivot_rot


    class Task8Scene(AnimatedScene):
        def __init__(self, **kwargs):
            kwargs["coordinate_rect"] = (-2, -5, -2, 10, 10, 15)
            kwargs["axis_show"] = False
            super().__init__(**kwargs)
            O = vertex(0, 0, 0)
            self["axis_x"] = Vector(O, vertex(10, 0, 0), color="red")
            self["axis_y"] = Vector(O, vertex(0, 10, 0), color="green")
            self["axis_z"] = Vector(O, vertex(0, 0, 10), color="blue")

            triangle = SimplePolygon(v0, v1, v2, color="orange", alpha=0.5)
            self[TRI_KEY] = triangle
            triangle.show_local_frame()
            triangle.show_pivot(True)

            target = SimplePolygon(v0, v1, v2, color="grey", alpha=0.2, line_style="-.")
            target.transformation = M_final
            self[TARGET_KEY] = target


    scene = Task8Scene(title="Завдання 8: Обертання навколо довільної осі через точку")
    scene[TRI_KEY].pivot(pivot_point.x, pivot_point.y, pivot_point.z)

    f = 60
    scene.add_animation(RotationAnimation(end=angle, axis=axis, frames=f, channel=TRI_KEY))
    scene.add_animation(TranslationAnimation(end=translation_vector, frames=f, channel=TRI_KEY))
    scene.show()