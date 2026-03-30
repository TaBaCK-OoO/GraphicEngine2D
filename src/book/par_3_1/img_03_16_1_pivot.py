import numpy as np

from engine.model.Point import SimplePoint
from engine.scene.Scene import Scene
from src.engine.model.Polygon import Polygon
from src.math.Mat3x3 import Mat3x3

ID = "ID"
ID_ORIG = "ID_ORIG"
LINE_WIDTH = 3.0

rectangle_vertices = [    # Вершини прямокутника
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

phi = np.deg2rad(45)
cos_phi = np.cos(phi)
sin_phi = np.sin(phi)
M = Mat3x3(
    2 * cos_phi, -2 * sin_phi,  0.5,
    2 * sin_phi,  2 * cos_phi, -1,
    0,            0,            1
)


S = Mat3x3.scale(2, 2)
R = Mat3x3.rotation(45, is_radians=False)
T = Mat3x3.translation(-0.5, -0.5)
M1 = T.inverse() * R * S * T

def frame_1(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.color = "grey"
    poligon.line_style = "--"

def frame_4(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = M
    poligon.color = "red"
    poligon.line_style = "-"

def frame_5(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = M1
    poligon.color = "blue"
    poligon.line_style = "--"


class SceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        rect = Polygon(
            rectangle_vertices,
            linewidth=LINE_WIDTH,
            color="red"
        )
        self[ID] = rect



if __name__ == '__main__':
    scene = SceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-2., -2, 2, 2),  # розмірність системи координат
        title="",  # заголовок рисунка
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
        # out_file ="img/05_vector.gif",    # шлях для запису анімації у файл
    )

    scene.add_frames(
        frame_1,
        frame_4,
        # frame_5,
    )

    scene.show()
