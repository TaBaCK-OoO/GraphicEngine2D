from base.arc import draw_arc
from base.text import print_label
from engine.model.Axis import Axis
from engine.model.LineModel import LineModel
from engine.scene.Scene import Scene

LABEL_FONT_SIZE = 20

if __name__ == '__main__':

    simple_scene = Scene(
        coordinate_rect=(-3.5, -3.5, 4, 3.5),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
    )

    z_dir = -1.4, -1.2

    v_dir = 1.6, 0.9
    v_proj_vert =  1.75, 0.95, 1.7, -0.8
    v_proj_oxy_ccords =  1.7, -0.8
    v_proj_z_coord = -0.9, -0.8
    v_proj_x_coord = 2.8, 0.0

    Ox = Axis(3.1, 0, color="red", linewidth=1.5, label="$x$", label_offset=(0.1, 0.1))
    Oy = Axis(0, 2.4, color="green", linewidth=1.5, label="$y$", label_offset=(0.1, 0.2))
    Oz = Axis(z_dir, color="blue", linewidth=1.5, label="$z$", label_offset=(-0.35, -0.3))
    v = Axis(v_dir, color="brown", linewidth=1.5, label="$v$", label_offset=(0.1, 0.2))
    v_proj_v = LineModel(*v_proj_vert, color="black", linewidth=1., line_style="--", )
    v_proj_oxy = LineModel((0, 0), v_proj_oxy_ccords, color="black", linewidth=1., line_style="--", )
    v_proj_z = LineModel(v_proj_oxy_ccords, v_proj_z_coord, color="black", linewidth=1., line_style="--", )
    v_proj_x = LineModel(v_proj_oxy_ccords, v_proj_x_coord, color="black", linewidth=1., line_style="--", )

    def frame1(scene: Scene):
        draw_arc((0, 0), z_dir, v_proj_oxy_ccords,
                 radius=0.25,
                 color="red",
                 linestyle="--",
                 linewidth=2.0,
                 )

        print_label(start= (-0.1, -0.3),
                    label=r"$\varphi$",
                    label_offset=(0.0, -0.2),
                    label_fontsize=LABEL_FONT_SIZE,
                    )

    simple_scene["OX"] = Ox
    simple_scene["OY"] = Oy
    simple_scene["OZ"] = Oz
    simple_scene["v"] = v
    simple_scene["v_proj_v"] = v_proj_v
    simple_scene["v_proj_oxy"] = v_proj_oxy
    simple_scene["v_proj_z"] = v_proj_z
    simple_scene["v_proj_x"] = v_proj_x

    simple_scene.add_frames(frame1)


    simple_scene.show()