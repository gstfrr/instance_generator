from abc import abstractmethod
import numpy as np


class AbstractPolyhedra:
    def __init__(self, vertex, faces, color=np.random.rand(1, 3), volume=0):
        self.__vertex = vertex
        self.__volume = volume
        self.__faces = faces
        self.__color = tuple(color)

    def rotate(self, alpha, beta):
        rotation_z = np.array([[np.cos(alpha), -1 * np.sin(alpha), 0],
                               [np.sin(alpha), np.cos(alpha), 0],
                               [0, 0, 1]])

        rotation_y = np.array([[np.cos(beta), 0, -1 * np.sin(beta)],
                               [0, 1, 0],
                               [np.sin(beta), 0, np.cos(beta)]])

        rotation = np.matmul(rotation_z, rotation_y)

        vertex = [*zip(*self.vertex)]

        new_v = []
        for i in vertex:
            v = np.matmul(rotation, i)
            new_v.append(tuple(v))

        new_v = [*zip(*new_v)]

        self.__vertex = new_v

    def save(self, index, total):

        v = [*zip(*self.vertex)]
        print('o\tpol_{0:03d}-{1:03d}'.format(index, total))
        for i in v:
            print('v', i[0], i[1], i[2], sep='\t')

        for i in self.faces:
            print('f\t', end='', sep='\t')
            for j in i:
                print(j + 1, end='\t')
            print('\n', end='')

        print('c\t', end='')
        for i in self.color:
            print(i, end='\t', sep='\t')

        print('\nd\t', end='')
        print('\n\n')

    @staticmethod
    def change_position(v_tuple, offset):
        coordinate_list = []
        for i in range(len(v_tuple)):
            coordinate_list.append(v_tuple[i] + offset)
        return tuple(coordinate_list)

    def change_vertex(self, offset):
        vertex_list = []
        for key, v in enumerate(self.__vertex):
            a = self.change_position(v, offset[key])
            vertex_list.append(a)

        self.__vertex = vertex_list

    def move_to_origin(self):
        minimo = np.array([min(self.vertex[0]), min(self.vertex[1]), min(self.vertex[2])])

        v = self.vertex

        c = []
        for i in range(len(v)):
            line = np.array(list(v[i])) - minimo[i]
            c.append(tuple(line))

        self.__vertex = c

    @property
    def vertex(self):
        return self.__vertex

    @property
    def faces(self):
        return self.__faces

    @property
    def color(self):
        return self.__color

    @property
    def volume(self):
        return self.__volume

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def show(self):
        print('vertex:\t', self.vertex)
        print('faces:\t', self.faces)
        print('color:\t', self.color)
