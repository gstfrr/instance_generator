import pyvoro
import numpy as np
import polygon as p


def get_vertices(vertex_dict):
    v = []
    for i in vertex_dict['vertices']:
        v.append(tuple(i))

    return [*zip(*v)]


def get_faces(l):
    f = []
    for i in l:
        f.append(i['vertices'])
    return f


class PolyGenerator:
    def __init__(self, seeds, x_lim, y_lim, z_lim):
        self.__seeds = seeds
        self.__x_lim = x_lim
        self.__y_lim = y_lim
        self.__z_lim = z_lim
        self.__polygon_array = None

    def get_polygons(self):
        polygons_array = []

        cells = self.get_cells()

        for key, cell in enumerate(cells):
            ve = get_vertices(cell)
            fa = get_faces(cell['faces'])
            # co = np.random.rand(self.__seeds, 3)
            seed = cell['original']

            polygon = p.Polygon(seed=seed,
                                vertex=ve,
                                faces=fa,
                                # color=co
                                )

            polygons_array.append(polygon)

        self.__polygon_array = polygons_array
        return self.__polygon_array

    def get_cells(self):
        cells = pyvoro.compute_voronoi(
            points=self.__seeds,
            limits=[self.__x_lim, self.__y_lim, self.__z_lim],
            dispersion=1
        )

        return cells
