git add src/homework/import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Mat3x3 import Mat3x3
from src.math.utils_matrix import decompose_affine3
from src.math.Vec3 import vertex

ID_ORIGINAL = "ID_ORIGINAL"
ID_RESTORED = "ID_RESTORED"

rectangle_vertices = [
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]


class Task14Scene(AnimatedScene):
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
            color="blue",
            line_style="-"
        )
        poly.pivot(1, 1)
        poly.show_pivot(True)
        poly.show_local_frame(True)
        self[ID_RESTORED] = poly


if __name__ == '__main__':
    T_total = Mat3x3(
        1.732, -1.0, 5.0,
        1.0, 1.732, -3.0,
        0, 0, 1.0
    )

    net_translation, angle, scales = decompose_affine3(T_total)

    S_mat = Mat3x3.scale(*scales)
    R_mat = Mat3x3.rotation(angle)
    T_pivot = Mat3x3.translation(1, 1)
    T_inv_pivot = Mat3x3.translation(-1, -1)

    M_pivot_effect = T_pivot * R_mat * S_mat * T_inv_pivot

    pure_translation = np.array(net_translation) - np.array([M_pivot_effect[0, 2], M_pivot_effect[1, 2]])

    scene = Task14Scene(
        image_size=(8, 8),
        coordinate_rect=(-2, -5, 8, 4),
        title="Завдання 14: Декомпозиція з pivot (1, 1)",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
    keep_aspect_ratio = True,
    )

    anim_s = ScaleAnimation(
        end=scales,
        channel=ID_RESTORED,
        apply_geometry_transformation_on_finish=True
    )
    anim_r = RotationAnimation(
        end=angle,
        channel=ID_RESTORED,
        apply_geometry_transformation_on_finish=True
    )
    anim_t = TranslationAnimation(
        end=vertex(*pure_translation),
        channel=ID_RESTORED,
        apply_geometry_transformation_on_finish=True
    )

    scene.add_animations(anim_s, anim_r, anim_t)
    scene.show()