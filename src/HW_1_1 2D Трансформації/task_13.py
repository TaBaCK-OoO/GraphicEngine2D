import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Mat3x3 import Mat3x3
from src.math.utils_matrix import decompose_affine3

ID_ORIGINAL = "ID_ORIGINAL"
ID_RESTORED = "ID_RESTORED"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class Task13Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIGINAL] = Polygon(rectangle_vertices, linewidth=2.0, color="grey", line_style="--")

        poly = Polygon(rectangle_vertices, linewidth=3.0, color="blue", line_style="-")
        poly.show_local_frame(True)
        self[ID_RESTORED] = poly


if __name__ == '__main__':

    T = Mat3x3(
        1.414, -2.121, 1.0,
        1.414,  2.121, 1.0,
        0,      0,     1.0
    )

    translation, angle, scales = decompose_affine3(T)

    print("--- Завдання 13: Декомпозиція TRS ---")
    print(f"Переміщення (Translation): {translation}")
    print(f"Поворот (Rotation, градуси): {np.degrees(angle):.1f}")
    print(f"Розтяг (Scale): {scales}")


    scene = Task13Scene(
        image_size=(8, 8),
        coordinate_rect=(-1, -1, 4, 5),
        title="Завдання 13: Розкладання матриці TRS",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    anim_s = ScaleAnimation(end=scales, channel=ID_RESTORED, apply_geometry_transformation_on_finish=True)
    anim_r = RotationAnimation(end=angle, channel=ID_RESTORED, apply_geometry_transformation_on_finish=True)
    anim_t = TranslationAnimation(end=translation, channel=ID_RESTORED, apply_geometry_transformation_on_finish=True)

    scene.add_animations(anim_s, anim_r, anim_t)
    scene.show()