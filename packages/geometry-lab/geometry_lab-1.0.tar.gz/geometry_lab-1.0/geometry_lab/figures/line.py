from math import sqrt


class Line:
    def __init__(self, point1, point2):
        self.__point_1 = point1
        self.__point_2 = point2

    @property
    def point_1(self):
        return self.__point_1

    @property
    def point_2(self):
        return self.__point_2

    def length(self):
        return sqrt(pow((self.__point_2.x - self.__point_1.x), 2) + pow((self.__point_2.y - self.__point_1.y), 2))
