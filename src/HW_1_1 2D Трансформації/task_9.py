import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Vec3 import vertex

ID_ORDER_1 = "ID_ORDER_1"
ID_ORDER_2 = "ID_ORDER_2"
ID_ORIGINAL = "ID_ORIGINAL"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task9Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIGINAL] = Polygon(
            rectangle_vertices,
            linewidth=1.0,
            color="grey",
            line_style="--"
        )

        # Квадрат для Порядку 1 (Розтяг -> Переміщення)[cite: 30, 31]
        poly1 = Polygon(rectangle_vertices, linewidth=2.0, color="blue", line_style="-")
        poly1.pivot(1, 1) # Опорна точка (1, 1)[cite: 32]
        poly1.show_pivot(True) # Візуалізація опорної точки[cite: 2, 32]
        self[ID_ORDER_1] = poly1

        # Квадрат для Порядку 2 (Переміщення -> Розтяг)[cite: 30, 31]
        poly2 = Polygon(rectangle_vertices, linewidth=2.0, color="red", line_style="--")
        poly2.pivot(1, 1) # Опорна точка (1, 1)[cite: 32]
        poly2.show_pivot(True) # Візуалізація опорної точки[cite: 2, 32]
        self[ID_ORDER_2] = poly2


if __name__ == '__main__':
    scene = Task9Scene(
        image_size=(10, 10),
        coordinate_rect=(-2, -4, 8, 3),
        title="Завдання 9: Розтяг і переміщення з опорною точкою (1, 1)",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    scale_params = (2, 1)
    trans_params = vertex(3, -2)

    # --- ПОРЯДОК 1: Розтяг (відносно pivot) → Переміщення (Синій) ---[cite: 30]
    s1 = ScaleAnimation(end=scale_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)
    t1 = TranslationAnimation(end=trans_params, channel=ID_ORDER_1, apply_geometry_transformation_on_finish=True)

    # --- ПОРЯДОК 2: Переміщення → Розтяг (відносно pivot) (Червоний) ---[cite: 30]
    t2 = TranslationAnimation(end=trans_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)
    s2 = ScaleAnimation(end=scale_params, channel=ID_ORDER_2, apply_geometry_transformation_on_finish=True)

    scene.add_animations(s1, t1, t2, s2)
    scene.show()