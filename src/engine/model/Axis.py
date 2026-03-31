import numpy as np

from engine.model.VectorModel import VectorModel
from engine.scene.Scene import Scene
from src.base.axes import draw_axis
from src.math.Mat3x3 import Mat3x3


class Axis(VectorModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_length_coef = 0.1
        self.head_width_coef = 0.05

    def __setitem__(self, key, value):
        if key == "head_width_coef":
            self.head_width_coef = value
            return
        if key == "head_length_coef":
            self.head_length_coef = value
            return

        super().__setitem__(key, value)

    def draw_model(self):
        transformed_geometry = self.transformed_geometry
        ps = [el.xyz for el in transformed_geometry]

        draw_axis(
            ps[0], # origin
            ps[1], # direction
            color=self.color[0],
            linewidth=self.linewidth,
            linestyle=self.line_style,
            head_length_coef=self.head_length_coef,
            head_width_coef=self.head_width_coef,
        )



if __name__ == '__main__':
    AXIS_KEY = "AXIS"

    R = Mat3x3.rotation(np.radians(30))
    S = Mat3x3.scale(0.5, 0.5)
    T = Mat3x3.translation(1, 0.5)



    ############## Frame 1 ##################
    def frame1(scene: Scene):
        rect: Axis = scene[AXIS_KEY]
        rect.line_style = "--"  # стиль ліній
        # rect.transformation = T * R #* S


    simple_scene = Scene(
        coordinate_rect=(-3, -3, 3, 3),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
        # axis_color="grey",  # колір осей координат
        # axis_line_style="-."  # стиль ліній осей координат
    )

    Ox = Axis(2, 0, color="red")
    Ox["line_style"] = "solid"
    simple_scene[AXIS_KEY] = Ox
    simple_scene.add_frames(frame1)

    simple_scene.show()