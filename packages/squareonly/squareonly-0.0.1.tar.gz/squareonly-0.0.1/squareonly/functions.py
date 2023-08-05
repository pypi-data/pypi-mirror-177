import math

def square_area(side):
        area = side*side
        print(area)


def ractangle_area(length, breath):
        area = length*breath
        print(area)


def circle_area(radius):
        area = float((3.14*(radius*radius)))
        print(float(area))


def right_angle_triangle_area(height, width):
        area = 1/2*(height*width)
        print(area)


def isosceles_triangle_area(breath, height):
        area = 1/2*(breath*height)
        print(area)


def equilateral_triangle_area(side):
        sq = math.sqrt(3)
        area = (sq/4)*side*side
        print('%.5f' % area)


def rombus_area(d1, d2):
        area = 1/2*(d1*d2)
        print(area)


def paralleogram_area(breath, height):
        area = breath*height
        print(area)


def trapezium_area(upper_b, lower_b, height):
        cal = 1/2*height
        area = cal*(upper_b*lower_b)
        print(area)


def hexagon_area(side):
        cal = math.sqrt(3)
        cal2 = (3*cal)/2
        area = cal2*side*side
        print('%.5f' % area)
