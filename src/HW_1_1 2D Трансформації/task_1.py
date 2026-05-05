import numpy as np

from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3

ID_ORIGINAL = "ID_ORIG"
ID_TRANSFORMED = "ID_TRANS"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task1Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIGINAL] = Polygon(
            rectangle_vertices,
            linewidth=2.0,
            color="grey",
            line_style="--"
        )

        self[ID_TRANSFORMED] = Polygon(
            rectangle_vertices,
            linewidth=3.0,
            color="blue"
        )


if __name__ == '__main__':
    scene = Task1Scene(
        image_size=(8, 8),
        coordinate_rect=(-2, -1, 4, 6),
        title="Завдання 1: Поворот і Переміщення",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    phi = np.deg2rad(30)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    R = Mat3x3(
        cos_phi, -sin_phi,   0,
        sin_phi,  cos_phi,   0,
              0,        0,   1
    )

    T = Mat3x3(
        1, 0, 2,
        0, 1, 3,
        0, 0, 1
    )

    scene.add_animations(
        TrsTransformationAnimation(end=R, channel=ID_TRANSFORMED, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=T, channel=ID_TRANSFORMED, apply_geometry_transformation_on_finish=True),
    )

    scene.show()