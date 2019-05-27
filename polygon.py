import numpy as np
import pywavefront


class Polygon:
    def __init__(self, seed, vertex, faces, color=None,volume=0):
        self.__seed = seed
        self.__vertex = vertex
        self.__faces = faces
        self.__color = color
        self.__volume = volume

    @staticmethod
    def load_polygons_from_file(obj_file):
        scene = pywavefront.Wavefront(obj_file, collect_faces=True)
        scene.parse()

        print(len(scene.vertices))

        print('# of objects:\t', len(scene.mesh_list))  # list of objects
        print('# of faces:\t', len(scene.mesh_list[0].faces))  # list of objects
        print(scene.mesh_list[0].faces)
        print(scene.vertices)

        # p = Polygon(seed=seed,
        #             vertex=vertex,
        #             faces=faces,
        #             color=color,
        #             )
        # return p

    @staticmethod
    def change_position(v_tuple, offset):
        coordinate_list = []
        for i in range(len(v_tuple)):
            coordinate_list.append(v_tuple[i] + offset)
        return tuple(coordinate_list)

    def rotate(self, alpha, beta):
        # alpha, beta = np.pi, np.pi

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

    @property
    def volume(self):
        return self.__volume

    def save(self, index, total):

        v = [*zip(*self.vertex)]
        print('o\tpol_{0:03d}-{1:03d}'.format(index, total))
        # print('# vertex')
        for i in v:
            print('v', i[0], i[1], i[2], sep='\t')

        # print('# faces')
        for i in self.faces:
            print('f\t', end='', sep='\t')
            # print('\n')
            for j in i:
                print(j + 1, end='\t')
            print('\n', end='')

        print('c\t', end='')
        for i in self.color:
            print(i, end='\t', sep='\t')

        print('\nd\t', end='')
        for i in self.seed:
            print(i, end='\t', sep='\t')

        print('\n\n')

    def show(self):
        print('seed:\t', self.seed)
        print('vertex:\t', self.vertex)
        print('faces:\t', self.faces)
        print('color:\t', self.color)
