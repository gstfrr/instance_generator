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
        self.alpha = alpha
        self.__line_ani = None

        self.__sfreq = None
        self.__button = None
        self.__text_box = None

        self.__ax = self.__fig.add_subplot(111,
                                           projection='3d',
                                           )
        self.new_scene()

    def new_scene(self):
        self.__ax.clear()
        # cube_vertex = [(0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 1, 1, 0, 0, 1, 1), (0, 0, 0, 0, 1, 1, 1, 1)]
        cube_vertex = [(0, self.__x_lim, 0, self.__x_lim, 0, self.__x_lim, 0, self.__x_lim),
                       (0, 0, self.__y_lim, self.__y_lim, 0, 0, self.__y_lim, self.__y_lim),
                       (0, 0, 0, 0, self.__z_lim, self.__z_lim, self.__z_lim, self.__z_lim)
                       ]
        self.add_vertex(vertices=cube_vertex)

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
        axfreq = plt.axes([.15, .05, .75, 0.03], facecolor='b')
        self.__sfreq = Slider(axfreq, 'Altura: ', -1.0, 1.0, valinit=0)

        resetax = plt.axes([0.8, .015, 0.1, 0.03])
        self.__button = Button(resetax, 'Reset', color='r', hovercolor='0.975')

        axbox = plt.axes([0.207, 0.015, 0.2, 0.03])
        self.__text_box = TextBox(axbox, 'Função Objetivo: ', initial=str(self.__obj))

        self.__sfreq.on_changed(self.update_polygons_height)
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
        collection = Poly3DCollection(verts2, alpha=self.alpha)
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
