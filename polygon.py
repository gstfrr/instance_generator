import numpy as np


class Polygon:
    def __init__(self, seed, vertex, faces, color=None):
        self.__seed = seed
        self.__vertex = vertex
        self.__faces = faces
        self.__color = color

    @staticmethod
    def change_position(v_tuple, offset):
        coordinate_list = []
        for i in range(len(v_tuple)):
            coordinate_list.append(v_tuple[i] + offset)
        return tuple(coordinate_list)

    def change_vertex(self, offset):
        print(self.__vertex)
        vertex_list = []
        for v in self.__vertex:
            # print(v)
            a = self.change_position(v, offset)
            vertex_list.append(a)

        self.__vertex = vertex_list

    def move_to_origin(self):
        minimo = np.array([min(self.vertex[0]), min(self.vertex[1]), min(self.vertex[2])])
        # print('Minimo:   ',minimo)

        v = self.vertex

        c = []
        for i in range(len(v)):
            line = np.array(list(v[i])) - minimo[i]
            # print(line)
            c.append(tuple(line))

        self.__vertex = c

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

    def save(self, folder, index, max):
        import sys
        path = '/Users/augusto/Drive/UFLA/Mestrado/TPS/instance_generator/' + folder
        filename = path + '/polygon-{0:04d}-{1:04d}.obj'.format(index, max)
        with open(filename, 'w') as f:
            sys.stdout = f

            v = [*zip(*self.vertex)]
            print('# vertex')
            for i in v:
                print('v', i[0], i[1], i[2], sep='\t')

            print('# faces')
            for i in self.faces:
                print('f\t', end='', sep='\t')
                # print('\n')
                for j in i:
                    print(j + 1, end='\t')
                print('\n', end='')

            print('# color\nc\t', end='')
            for i in self.color:
                print(i, end='\t', sep='\t')

    def show(self):
        print('seed:\t', self.seed)
        print('vertex:\t', self.vertex)
        print('faces:\t', self.faces)
        print('color:\t', self.color)
