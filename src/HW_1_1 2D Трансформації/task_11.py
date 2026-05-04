import numpy as np

from src.engine.scene.AnimatedScene import AnimatedScene
from src.engine.model.Polygon import Polygon
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.math.Mat3x3 import Mat3x3
from src.math.utils_matrix import decompose_affine3
from src.math.Vec3 import vertex

ID_GLOBAL = "ID_GLOBAL"
ID_LOCAL = "ID_LOCAL"

# Вершини після трансформації (глобальна система)[cite: 28, 44]
transformed_vertices = [
    2.0, 3.4,
    4.9, 4.0,
    4.5, 6.0,
    1.6, 5.4
]


class Task11Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Прямокутник у глобальній системі координат (трансформований, червоний пунктир)[cite: 32, 40]
        self[ID_GLOBAL] = Polygon(
            transformed_vertices,
            linewidth=2.0,
            color="red",
            line_style="--"
        )

        # Прямокутник, який ми повернемо в локальну систему координат (синій)[cite: 32]
        self[ID_LOCAL] = Polygon(
            transformed_vertices,
            linewidth=3.0,
            color="blue",
            line_style="-"
        )


if __name__ == '__main__':
    scene = Task11Scene(
        image_size=(8, 8),
        coordinate_rect=(-1, -1, 7, 7),
        title="Завдання 11: Відновлення початкового зображення",
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    # 1. Задана матриця трансформацій T[cite: 29, 30]
    T = Mat3x3(
        2.934, -0.416, 2.000,
        0.624, 1.956, 3.400,
        0, 0, 1
    )

    # Замість анімації зворотної матриці напряму,
    # декомпозуємо оригінальну матрицю на складові (T, R, S)[cite: 21]
    orig_translation, orig_angle, orig_scales = decompose_affine3(T)

    print("--- 1. Оригінальні компоненти (T, R, S) ---")
    print(f"Переміщення: {orig_translation}")
    print(f"Кут (рад): {orig_angle}")
    print(f"Масштаб: {orig_scales}\n")

    # 2. Розраховуємо зворотні компоненти
    inv_translation = vertex(-orig_translation[0], -orig_translation[1])
    inv_angle = -orig_angle
    inv_scale = (1.0 / orig_scales[0], 1.0 / orig_scales[1])

    # 3. Визначаємо зворотну матрицю T_inv суто для перевірки координат[cite: 28, 36]
    T_inv = T.inverse()
    print("--- 2. Координати в локальній системі ---")
    for i in range(0, len(transformed_vertices), 2):
        x = transformed_vertices[i]
        y = transformed_vertices[i + 1]
        local_vec = T_inv * vertex(x, y)
        print(f"P{i // 2 + 1} Глобальна: ({x}, {y}) -> Локальна: ({local_vec.x:.1f}, {local_vec.y:.1f})")

    # 4. Анімація відновлення початкового положення
    # Оскільки оригінальний порядок був S -> R -> T,
    # зворотний порядок має бути: Переміщення^-1 -> Поворот^-1 -> Розтяг^-1

    anim_trans = TranslationAnimation(
        end=inv_translation,
        channel=ID_LOCAL,
        apply_geometry_transformation_on_finish=True  # Застосовуємо трансформацію до геометрії[cite: 30, 44]
    )

    anim_rot = RotationAnimation(
        end=inv_angle,
        channel=ID_LOCAL,
        apply_geometry_transformation_on_finish=True  # Застосовуємо трансформацію до геометрії[cite: 30, 44]
    )

    anim_scale = ScaleAnimation(
        end=inv_scale,
        channel=ID_LOCAL,
        apply_geometry_transformation_on_finish=True  # Застосовуємо трансформацію до геометрії[cite: 30, 44]
    )

    scene.add_animations(anim_trans, anim_rot, anim_scale)
    scene.show()