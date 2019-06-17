import numpy as np
from abstract_polyhedra import AbstractPolyhedra


class Polygon(AbstractPolyhedra):
    def __init__(self, vertex, faces, color=None, volume=0):
        self.__vertex = vertex
        self.__faces = faces
        self.__color = tuple(color)
        self.__volume = volume
        super().__init__(vertex=vertex, faces=self.__faces, color=color, volume=volume)
