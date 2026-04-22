from src.math.Vec4 import vertex  # ДОДАНО ЦЕЙ ІМПОРТ
from src.engine.model.Model import Model
from src.engine.model.SimplePolygon import SimplePolygon


class Tetrahedron(Model):

    def __init__(self,
                 alpha=1.0,
                 color="orange",
                 edge_color="black",
                 line_style="-",
                 line_width=1.0,
                 ):
        # Визначаємо вершини тетраедра
        v0, v1, v2, v3 = vertex(0, 0, 0), vertex(1, 0, 0), vertex(0, 1, 0), vertex(0, 0, 1)

        # ПЕРЕДАЄМО вершини в батьківський клас BaseModel для ініціалізації self._geometry
        super().__init__(v0, v1, v2, v3, color=color)

        self.polygons = []
        faces = [[v0, v1, v2], [v0, v1, v3], [v0, v2, v3], [v1, v2, v3]]

        for face in faces:
            self.polygons.append(
                SimplePolygon(*face, color=color, edgecolor=edge_color, alpha=alpha)
            )

    def draw_model(self, plt_axis):
        for polygon in self.polygons:
            polygon.transformation = self.transformation
            polygon.pivot(self._pivot)
            polygon.draw(plt_axis)

    def apply_transformation_to_geometry(self):
        super().apply_transformation_to_geometry()
        for polygon in self.polygons:
            polygon.apply_transformation_to_geometry()