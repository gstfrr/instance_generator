import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class PolyVisualiser:
    """
        Construtor da Classe
        :param array_polygons: lista de polígonos a serem exibidos (Retângulos ou Polígonos)
        :param x_lim: máxima largura da área de visualização.
        :param y_lim: máxima comprimento da área de visualização.
        :param z_lim: máxima altura da área de visualização.
        :param obj: (opcional) Valor da função objetivo a ser exibido.
    """

    def __init__(self, array_polygons, x_lim, y_lim, z_lim, obj=0, alpha=.5, title='Visualizador'):
        self.__array_polygons = array_polygons
        self.__x_lim = x_lim
        self.__y_lim = y_lim
        self.__z_lim = z_lim
        self.__obj = obj
        self.__title = title
        self.__fig = plt.figure(figsize=(9, 6.5), num=self.__title)
        self.__alpha = alpha
        self.__line_ani = None

        self.__sfreq = None
        self.__button = None
        self.__text_box = None

        self.__ax = self.__fig.add_subplot(111,
                                           projection='3d',
                                           )
        self.__ax.tick_params(direction='out', length=6, width=2, colors='r',
                              grid_color='r', grid_alpha=0.5, grid_linewidth=5)
        self.new_scene()

    def new_scene(self):
        self.__ax.clear()
        # cube_vertex = [(0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 1, 1, 0, 0, 1, 1), (0, 0, 0, 0, 1, 1, 1, 1)]
        cube_vertex = [(0, self.__x_lim, 0, self.__x_lim, 0, self.__x_lim, 0, self.__x_lim),
                       (0, 0, self.__y_lim, self.__y_lim, 0, 0, self.__y_lim, self.__y_lim),
                       (0, 0, 0, 0, self.__z_lim, self.__z_lim, self.__z_lim, self.__z_lim)
                       ]
        self.add_vertex(vertices=cube_vertex)

    def update_polygons_alpha(self, val):
        self.new_scene()
        self.__alpha = self.__salpha.val
        self.add_cell(vertex=False, faces=True)

    def update_polygons_height(self, val):
        self.new_scene()
        freq = self.__sfreq.val
        for p in self.__array_polygons:
            min_z = min(p.vertex[2])
            a = np.array(list(p.vertex[2])) + (min_z * freq)
            # print(a)

            p.vertex[2] = tuple(a)

        self.add_cell(vertex=False, faces=True)

    def reset(self, event):
        pass

    def scrol(self):
        axfreq = plt.axes([.15, .05, .25, .03], facecolor='b')
        self.__sfreq = Slider(axfreq, 'Altura: ', -1.0, 1.0, valinit=0)

        axtransp = plt.axes([.65, .05, .25, .03], facecolor='b')
        self.__salpha = Slider(axtransp, 'Alpha: ', 0, 1.0, valinit=1)

        resetax = plt.axes([.8, .015, 0.1, .03])
        self.__button = Button(resetax, 'Reset', color='r', hovercolor='0.975')

        axbox = plt.axes([.207, .015, .2, .03])
        self.__text_box = TextBox(axbox, 'Função Objetivo: ', initial=str(self.__obj))

        self.__sfreq.on_changed(self.update_polygons_height)
        self.__salpha.on_changed(self.update_polygons_alpha)
        self.__button.on_clicked(self.reset)
        self.__text_box.on_submit(None)

    def add_cell(self, vertex=False, faces=True):
        for p in self.__array_polygons:
            vertices = p.vertex
            face = p.faces
            color = p.color
            if vertex:
                self.add_vertex(vertices, color)
            if faces:
                self.add_faces(vertices, face, color)

    def add_vertex(self, vertices, color='w'):
        self.__ax.scatter(
            vertices[0], vertices[1], vertices[2],
            c=color,
            marker='.',
            alpha=0
        )

    def add_plane(self, a, b, c):
        points = [a, b, c]

        p0, p1, p2 = points
        x0, y0, z0 = p0
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        ux, uy, uz = [x1 - x0, y1 - y0, z1 - z0]
        vx, vy, vz = [x2 - x0, y2 - y0, z2 - z0]
        u_cross_v = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx]
        point = np.array(p0)
        normal = np.array(u_cross_v)
        d = -point.dot(normal)
        xx, yy = np.meshgrid(range(20), range(20))

        z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

        self.__ax.plot_surface(xx, yy, z, color='r', shade=False, alpha=.5)

        self.__ax.scatter(a[0], a[1], a[2])
        self.__ax.scatter(b[0], b[1], b[2])
        self.__ax.scatter(c[0], c[1], c[2])

    def add_faces(self, vertices, faces, color):
        vertices = [*zip(*vertices)]
        for f in faces:
            augusto = []
            for i in f:
                augusto.append(vertices[i])
            self.new_face(augusto, color)

    def new_face(self, augusto, color):
        augusto = [*zip(*augusto)]
        x, y, z = augusto
        verts2 = [list(zip(x, y, z))]
        collection = Poly3DCollection(verts2, alpha=self.__alpha)
        collection.set_facecolor(color)
        collection.set_edgecolor('k')
        self.__ax.add_collection3d(collection, zs=0, zdir='z')
        return None

    def update_lines(self, num):
        p = self.__array_polygons[num]
        # self.add_vertex(p.vertex, p.color)
        self.add_faces(p.vertex, p.faces, p.color)

    def animate(self, no_animation=False):
        if no_animation:
            self.add_cell()
            return

        num_frames = len(self.__array_polygons)
        self.__line_ani = animation.FuncAnimation(fig=self.__fig,
                                                  func=self.update_lines,
                                                  frames=num_frames,
                                                  interval=100,
                                                  repeat=False
                                                  )

    @staticmethod
    def show():
        plt.show()
