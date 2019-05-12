import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import colors, animation


class PolyVisualiser:
    def __init__(self, array_polygons, x_lim, y_lim, z_lim):
        self.__array_polygons = array_polygons
        self.__x_lim = x_lim
        self.__y_lim = y_lim
        self.__z_lim = z_lim
        self.__fig = plt.figure(figsize=(10, 6.5))
        self.__ax = self.__fig.add_subplot(111, projection='3d', aspect='equal')
        self.__line_ani = None

    def add_seeds(self, points):

        self.__ax.scatter(
            points[0], points[1], points[2],
            c='b',
            marker='o',
            alpha=1
        )

    def add_cell(self, vertex=True, faces=True):
        for p in self.__array_polygons:
            vertices = p.vertex
            face = p.faces
            color = p.color
            seed = p.seed
            self.add_seeds(seed)
            if vertex:
                self.add_vertex(vertices)
            if faces:
                self.add_faces(vertices, face, color)

    def add_vertex(self, vertices):
        self.__ax.scatter(
            vertices[0], vertices[1], vertices[2],
            c='k',
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
        x = augusto[0]
        y = augusto[1]
        z = augusto[2]
        verts2 = [list(zip(x, y, z))]
        collection = Poly3DCollection(verts2, alpha=0.33)
        collection.set_facecolor(color)
        collection.set_edgecolor(color)
        self.__ax.add_collection3d(collection, zs='z')
        return None

    def update_lines(self, num):
        p = self.__array_polygons[num]
        self.add_seeds(p.seed)
        self.add_vertex(p.vertex)
        self.add_faces(p.vertex, p.faces, p.color)

    def animate(self):
        frames = len(self.__array_polygons)
        self.__line_ani = animation.FuncAnimation(fig=self.__fig,
                                                  func=self.update_lines,
                                                  frames=frames,
                                                  interval=1000,
                                                  repeat=False
                                                  )

    @staticmethod
    def show():
        plt.show()
