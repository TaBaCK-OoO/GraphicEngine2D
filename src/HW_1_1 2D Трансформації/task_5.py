import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Vec3 import vertex

ID_ORIGINAL = "ID_ORIG"
ID_TRANSFORMED = "ID_TRANS"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task5Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIGINAL] = Polygon(
            rectangle_vertices,
            linewidth=2.0,
            color="grey",
            line_style="--"
        )

        poly = Polygon(
            rectangle_vertices,
            linewidth=3.0,
            color="blue"
        )
        poly.show_local_frame(True)
        self[ID_TRANSFORMED] = poly


if __name__ == '__main__':
    scene = Task5Scene(
        image_size=(8, 8),
        coordinate_rect=(-1, -3, 5, 3),
        title="Завдання 5: Переміщення та Масштабування",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    anim_trans = TranslationAnimation(
        end=vertex(1, -1),
        channel=ID_TRANSFORMED,
        apply_geometry_transformation_on_finish=True
    )

    anim_scale = ScaleAnimation(
        end=(2, 2),
        channel=ID_TRANSFORMED,
        apply_geometry_transformation_on_finish=True
    )

    scene.add_animations(anim_trans, anim_scale)
    scene.show()