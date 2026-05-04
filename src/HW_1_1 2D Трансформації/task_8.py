import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation

ID_PIVOT_1 = "ID_PIVOT_1"
ID_PIVOT_2 = "ID_PIVOT_2"
ID_PIVOT_3 = "ID_PIVOT_3"
ID_PIVOT_4 = "ID_PIVOT_4"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]


class Task8Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Опорна точка 1: (0.5, 0.5)[cite: 32]
        poly1 = Polygon(rectangle_vertices, linewidth=2.0, color="blue", line_style="-")
        poly1.pivot(0.5, 0.5)
        poly1.show_pivot(True)
        self[ID_PIVOT_1] = poly1

        # Опорна точка 2: (0, 1)[cite: 32]
        poly2 = Polygon(rectangle_vertices, linewidth=2.0, color="red", line_style="--")
        poly2.pivot(0, 1)
        poly2.show_pivot(True)
        self[ID_PIVOT_2] = poly2

        # Опорна точка 3: (1, 1)[cite: 32]
        poly3 = Polygon(rectangle_vertices, linewidth=2.0, color="green", line_style=":")
        poly3.pivot(1, 1)
        poly3.show_pivot(True)
        self[ID_PIVOT_3] = poly3

        # Опорна точка 4: (2, 2)[cite: 32]
        poly4 = Polygon(rectangle_vertices, linewidth=2.0, color="orange", line_style="-.")
        poly4.pivot(2, 2)
        poly4.show_pivot(True)
        self[ID_PIVOT_4] = poly4


if __name__ == '__main__':
    scene = Task8Scene(
        image_size=(10, 10),
        coordinate_rect=(-4, -5, 4, 4),  # Розширено межі, щоб вмістити розтяг від (2, 2)[cite: 33]
        title="Завдання 8: Розтяг навколо опорної точки (pivot)",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    scale_params = (2, 3)

    # Анімації розтягу для кожного випадку[cite: 48]
    anim1 = ScaleAnimation(end=scale_params, channel=ID_PIVOT_1, apply_geometry_transformation_on_finish=True)
    anim2 = ScaleAnimation(end=scale_params, channel=ID_PIVOT_2, apply_geometry_transformation_on_finish=True)
    anim3 = ScaleAnimation(end=scale_params, channel=ID_PIVOT_3, apply_geometry_transformation_on_finish=True)
    anim4 = ScaleAnimation(end=scale_params, channel=ID_PIVOT_4, apply_geometry_transformation_on_finish=True)

    scene.add_animations(anim1, anim2, anim3, anim4)
    scene.show()