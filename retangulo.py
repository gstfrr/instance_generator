from abstract_polyhedra import AbstractPolyhedra
import numpy as np


class Retangulo(AbstractPolyhedra):
    def __init__(self, vertex, color=np.random.rand(1, 3)):
        vol = vertex[0] * vertex[1] * vertex[2]

        vertices = [[0.0, 0.0, 0.0],
                    [vertex[0], 0.0, 0.0],
                    [0.0, vertex[1], 0.0],
                    [vertex[0], vertex[1], 0.0],
                    [0.0, 0.0, vertex[2]],
                    [vertex[0], 0.0, vertex[2]],
                    [0.0, vertex[1], vertex[2]],
                    [vertex[0], vertex[1], vertex[2]]]

        vertices = [*zip(*vertices)]

        self.__faces = [[1, 3, 2, 0],
                        [1, 5, 7, 3],
                        [1, 0, 4, 5],
                        [2, 6, 4, 0],
                        [2, 3, 7, 6],
                        [4, 6, 7, 5]]

        super().__init__(vertex=vertices, faces=self.__faces, color=color, volume=vol)
