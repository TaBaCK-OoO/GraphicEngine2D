import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.RotationAnimation import RotationAnimation

ID_ORIGINAL = "ID_ORIG"
ID_TRANSFORMED = "ID_TRANS"
rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task2Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Оригінальний квадрат (сірий, пунктир)[cite: 32]
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
    scene = Task2Scene(
        image_size=(8, 8),
        coordinate_rect=(-2, -1, 4, 4),
        title="Завдання 2: Розтяг і Поворот",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    anim_scale = ScaleAnimation(
        end=(2, 1),
        channel=ID_TRANSFORMED,
        apply_geometry_transformation_on_finish=True
    )
    anim_rot = RotationAnimation(
        end=np.radians(45),
        channel=ID_TRANSFORMED,
        apply_geometry_transformation_on_finish=True
    )

    scene.add_animations(anim_scale, anim_rot)
    scene.show()