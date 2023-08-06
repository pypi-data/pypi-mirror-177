from .line import Line


class Triangle:
    def __init__(self, p1, p2, p3):
        if 0.5 * abs(((p1.x - p3.x) * (p2.y - p3.y)) - ((p2.x - p3.x) * (p1.y - p3.y))) == 0:
            raise ValueError("Triangle does not exist!")
        self.__point_1 = p1
        self.__point_2 = p2
        self.__point_3 = p3

    @property
    def point_1(self):
        return self.__point_1

    @property
    def point_2(self):
        return self.__point_2

    @property
    def point_3(self):
        return self.__point_3

    def perimeter(self):
        line1 = Line(self.__point_1, self.__point_2).length()
        line2 = Line(self.__point_2, self.__point_3).length()
        line3 = Line(self.__point_1, self.__point_3).length()
        return round((line1 + line2 + line3), 4)

    def square(self):
        x1 = self.__point_1.x
        y1 = self.__point_1.y
        x2 = self.__point_2.x
        y2 = self.__point_2.y
        x3 = self.__point_3.x
        y3 = self.__point_3.y
        return round(0.5 * abs(((x1 - x3) * (y2 - y3)) - ((x2 - x3) * (y1 - y3))), 4)
