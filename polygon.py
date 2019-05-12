class Polygon:
    def __init__(self, seed, vertex, faces, color=None):
        self.__seed = seed
        self.__vertex = vertex
        self.__faces = faces
        self.__color = seed

    @property
    def seed(self):
        return self.__seed

    @property
    def vertex(self):
        return self.__vertex

    @property
    def faces(self):
        return self.__faces

    @property
    def color(self):
        return self.__color

    def show(self):
        print('seed:\t', self.seed)
        print('vertex:\t', self.vertex)
        print('faces:\t', self.faces)
        print('color:\t', self.color)
