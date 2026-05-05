
import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Vec3 import vertex

ID_ORIGINAL = "ID_ORIGINAL"
ID_ORDER_1 = "ID_ORDER_1"
ID_ORDER_2 = "ID_ORDER_2"
ID_ORDER_3 = "ID_ORDER_3"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task10Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIGINAL] = Polygon(
            rectangle_vertices,
            linewidth=1.0,
            color="grey",
            line_style="--"
        )


        poly1 = Polygon(rectangle_vertices, linewidth=2.0, color="blue", line_style="-")
        poly1.pivot(0.5, 0.5)
        poly1.show_pivot(True)
        self[ID_ORDER_1] = poly1


        poly2 = Polygon(rectangle_vertices, linewidth=2.0, color="red", line_style="--")
        poly2.pivot(0.5, 0.5)
        poly2.show_pivot(True)
        self[ID_ORDER_2] = poly2


        poly3 = Polygon(rectangle_vertices, linewidth=2.0, color="green", line_style=":")
        poly3.pivot(0.5, 0.5)
        poly3.show_pivot(True)
        self[ID_ORDER_3] = poly3


if __name__ == '__main__':
    scene = Task10Scene(
        image_size=(10, 10),
        coordinate_rect=(-3, -5, 6, 4),
        title="Завдання 10: Зсув і масштабування (pivot 0.5, 0.5)",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    scale_params = (2, 2)
    rot_params = np.radians(30)
    trans_params = vertex(1, -1)

    # --- ПОРЯДОК 1: Масштабування -> Обертання -> Зсув ---
    s1 = ScaleAnimation(end=scale_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)
    r1 = RotationAnimation(end=rot_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)
    t1 = TranslationAnimation(end=trans_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)

    # --- ПОРЯДОК 2: Зсув -> Масштабування -> Обертання ---
    t2 = TranslationAnimation(end=trans_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)
    s2 = ScaleAnimation(end=scale_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)
    r2 = RotationAnimation(end=rot_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)

    # --- ПОРЯДОК 3: Масштабування -> Зсув -> Обертання ---
    s3 = ScaleAnimation(end=scale_params, channel=ID_ORDER_3, apply_geometry_transformation_on_finish=True)
    t3 = TranslationAnimation(end=trans_params, channel=ID_ORDER_3, apply_geometry_transformation_on_finish=True)
    r3 = RotationAnimation(end=rot_params, channel=ID_ORDER_3, apply_geometry_transformation_on_finish=True)

    scene.add_animations(s1, r1, t1, t2, s2, r2, s3, t3, r3)
    scene.show()