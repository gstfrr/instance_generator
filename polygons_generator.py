import pyvoro
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
    """
        Construtor da classe.
        :param seeds: Porta serial do dispositivo USB GPS
        :param x_lim: limite x máximo do paralelepipedo a ser gerado
        :param y_lim: limite y máximo do paralelepipedo a ser gerado
        :param z_lim: limite x máximo do paralelepipedo a ser gerado
        :param scale: escada do paralelepipedo (default=1)
    """

    def __init__(self, seeds, x_lim, y_lim, z_lim, scale=1):
        self.__seeds = seeds
        self.__x_lim = x_lim
        self.__y_lim = y_lim
        self.__z_lim = z_lim
        self.__scale = scale
        self.__polygon_array = None

    def get_polygons(self) -> list:
        """"
            Método para extrair os polígonos das células geradas pelo método get_cells
            :return: list do tipo Polygons
        """
        polygons_array = []

        cells = self.get_cells()

        for key, cell in enumerate(cells):
            ve = get_vertices(cell)
            fa = get_faces(cell['faces'])
            seed = cell['original']
            volume = cell['volume']

            polygon = p.Polygon(vertex=ve,
                                faces=fa,
                                color=seed / self.__scale,
                                volume=volume
                                )

            polygons_array.append(polygon)

        self.__polygon_array = polygons_array
        return self.__polygon_array

    def get_cells(self) -> dict:
        """
            Retorna um dicionário de células geradas pelo PyVoro .
            :return: dicionário contendo as células geradas pelo PyVoro
        """
        cells = pyvoro.compute_voronoi(
            points=self.__seeds,
            limits=[self.__x_lim, self.__y_lim, self.__z_lim],
            dispersion=1,
            radii=[],
            periodic=[False] * 3,
        )

        return cells
