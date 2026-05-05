import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.RotationAnimation import RotationAnimation

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

class Task7Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        poly1 = Polygon(rectangle_vertices, linewidth=2.0, color="blue", line_style="-")
        poly1.pivot(0.5, 0.5)
        poly1.show_pivot(True) # Візуалізація опорної точки[cite: 2, 32]
        self[ID_PIVOT_1] = poly1

        poly2 = Polygon(rectangle_vertices, linewidth=2.0, color="red", line_style="--")
        poly2.pivot(0, 1)
        poly2.show_pivot(True) # Візуалізація опорної точки[cite: 2, 32]
        self[ID_PIVOT_2] = poly2

        poly3 = Polygon(rectangle_vertices, linewidth=2.0, color="green", line_style=":")
        poly3.pivot(1, 1)
        poly3.show_pivot(True) # Візуалізація опорної точки[cite: 2, 32]
        self[ID_PIVOT_3] = poly3

        poly4 = Polygon(rectangle_vertices, linewidth=2.0, color="yellow", line_style="--")
        poly4.pivot(2, 2)
        poly4.show_pivot(True)  # Візуалізація опорної точки[cite: 2, 32]
        self[ID_PIVOT_4] = poly4


if __name__ == '__main__':
    scene = Task7Scene(
        image_size=(10, 10),
        coordinate_rect=(-2, -1, 3, 3),
        title="Завдання 7: Поворот навколо опорної точки (pivot)",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    rot_angle = np.radians(60)

    anim1 = RotationAnimation(end=rot_angle, channel=ID_PIVOT_1, apply_geometry_transformation_on_finish=True)
    anim2 = RotationAnimation(end=rot_angle, channel=ID_PIVOT_2, apply_geometry_transformation_on_finish=True)
    anim3 = RotationAnimation(end=rot_angle, channel=ID_PIVOT_3, apply_geometry_transformation_on_finish=True)
    anim4 = RotationAnimation(end=rot_angle, channel=ID_PIVOT_4, apply_geometry_transformation_on_finish=True)

    scene.add_animations(anim1, anim2, anim3, anim4)
    scene.show()