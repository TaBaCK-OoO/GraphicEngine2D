import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Tetrahedron import Tetrahedron  # Наш новий клас!
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    TETRAHEDRON_KEY = "tetra"
    TARGET_KEY = "tetra_target"

    # --- 1. ГЕНЕРАЦІЯ ВИПАДКОВИХ ПАРАМЕТРІВ ---

    # Випадковий кут від 10° до 90°
    angle_deg = np.random.uniform(10, 90)
    angle_rad = np.radians(angle_deg)

    # Випадкова вісь (x, y, z)
    rand_axis = np.random.uniform(-1, 1, 3)
    axis_norm = rand_axis / np.linalg.norm(rand_axis)  # Обов'язкова нормалізація
    axis = Vec4(axis_norm[0], axis_norm[1], axis_norm[2])

    # Випадковий вектор переміщення від -5 до 5
    tx, ty, tz = np.random.uniform(-5, 5, 3)
    translation_vector = Vec3(tx, ty, tz)

    # Виводимо параметри в консоль
    print(f"--- Рандомізовані параметри ---")
    print(f"Кут обертання: {angle_deg:.2f}°")
    print(f"Вісь обертання (нормалізована): ({axis_norm[0]:.3f}, {axis_norm[1]:.3f}, {axis_norm[2]:.3f})")
    print(f"Вектор зсуву: ({tx:.2f}, {ty:.2f}, {tz:.2f})\n")

    # --- 2. ПОБУДОВА МАТРИЦЬ ---
    R = Mat4x4.rotation(angle_rad, axis, is_radians=True)
    T = Mat4x4.translation(translation_vector)

    # Результуюча матриця: Обертання -> Переміщення
    M_final = T * R


    class TetrahedronScene(AnimatedScene):
        def __init__(self, **kwargs):
            # Розширюємо межі камери, оскільки об'єкт може полетіти куди завгодно в межах [-5, 5]
            kwargs["coordinate_rect"] = (-2, -2, -2, 5, 5, 5)
            kwargs["axis_show"] = False
            super().__init__(**kwargs)

            # Кастомні кольорові осі
            O = vertex(0, 0, 0)
            self["axis_x"] = Vector(O, vertex(6, 0, 0), color="red")
            self["axis_y"] = Vector(O, vertex(0, 6, 0), color="green")
            self["axis_z"] = Vector(O, vertex(0, 0, 6), color="blue")

            # Використовуємо наш новий повноцінний 3D Тетраедр
            tetrahedron = Tetrahedron(color="orange", edge_color="black", alpha=0.5)
            self[TETRAHEDRON_KEY] = tetrahedron
            tetrahedron.show_local_frame()

            # Створюємо мішень у фінальній точці
            target = Tetrahedron(color="grey", edge_color="grey", alpha=0.2, line_style="-.")
            target.transformation = M_final
            self[TARGET_KEY] = target


    animated_scene = TetrahedronScene(title="Task 5: Randomized Rotation and Translation")
    frames_num = 60

    # --- 3. АНІМАЦІЇ ---

    # Етап 1: Обертання навколо випадкової осі
    anim_rot = RotationAnimation(
        end=angle_rad,
        axis=axis,
        frames=frames_num,
        channel=TETRAHEDRON_KEY
    )

    # Етап 2: Випадкове переміщення
    anim_trans = TranslationAnimation(
        end=translation_vector,
        frames=frames_num,
        channel=TETRAHEDRON_KEY
    )

    # Додаємо анімації у сцену
    animated_scene.add_animation(anim_rot)
    animated_scene.add_animation(anim_trans)

    animated_scene.show()