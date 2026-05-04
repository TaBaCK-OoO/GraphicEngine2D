import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Vec3 import vertex

ID_ORIGINAL = "ID_ORIG"
ID_ORDER_1 = "ID_ORDER_1"
ID_ORDER_2 = "ID_ORDER_2"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task6Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIGINAL] = Polygon(
            rectangle_vertices,
            linewidth=2.0,
            color="grey",
            line_style="--"
        )

        poly1 = Polygon(
            rectangle_vertices,
            linewidth=3.0,
            color="blue",
            line_style="-"
        )
        poly1.show_local_frame(True)
        self[ID_ORDER_1] = poly1

        poly2 = Polygon(
            rectangle_vertices,
            linewidth=3.0,
            color="red",
            line_style="--"
        )
        poly2.show_local_frame(True)
        self[ID_ORDER_2] = poly2


if __name__ == '__main__':
    scene = Task6Scene(
        image_size=(10, 10),
        coordinate_rect=(-12, -2, 6, 12),
        title="Завдання 6: Композиція 3-х трансформацій (2 порядки)",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    scale_params = (1, 3)
    rot_params = np.radians(60)
    trans_params = vertex(2, 3)

    # --- ПОРЯДОК 1: Розтяг -> Поворот -> Переміщення (Синій) ---
    s1 = ScaleAnimation(end=scale_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)
    r1 = RotationAnimation(end=rot_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)
    t1 = TranslationAnimation(end=trans_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)

    # --- ПОРЯДОК 2: Переміщення -> Розтяг -> Поворот (Червоний) ---
    t2 = TranslationAnimation(end=trans_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)
    s2 = ScaleAnimation(end=scale_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)
    r2 = RotationAnimation(end=rot_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)

    scene.add_animations(s1, r1, t1, t2, s2, r2)
    scene.show()