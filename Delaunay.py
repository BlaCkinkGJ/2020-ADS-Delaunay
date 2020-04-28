import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from sympy.geometry import *

points = []

file = open("points.txt", "r")
lines = file.readlines()
lines = [line.strip() for line in lines]
N = int(lines[0])
for index in range(1, N + 1):
    points += [[int(item) for item in lines[index].split()]]
file.close()

points = np.array(points)

for i in range(len(points)):
    ptxt = str(i) + "(" + str(points[i][0]) + "," + str(points[i][1]) + ")"
    plt.annotate(ptxt, (points[i][0], points[i][1]), fontsize=9, fontweight='bold')


def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def is_inside(cp, _p1, _p2, _p3):
    x, y = cp
    x1, y1 = _p1
    x2, y2 = _p2
    x3, y3 = _p3

    a = area(x1, y1, x2, y2, x3, y3)
    a1 = area(x, y, x2, y2, x3, y3)
    a2 = area(x1, y1, x, y, x3, y3)
    a3 = area(x1, y1, x2, y2, x, y)

    if a == a1 + a2 + a3:
        return True
    else:
        return False


tri = Delaunay(points)

plt.triplot(points[:, 0], points[:, 1], tri.simplices.copy())
plt.plot(points[:, 0], points[:, 1], 'o')

#                from    to
line = np.array([[2, 2], [12, 8]])  # 이 값을 변경해주세요.
plt.plot(line[:, 0], line[:, 1])

result = []
for p in tri.simplices:
    # line
    P1, P2 = Point(line[0, 0], line[0, 1]), Point(line[1, 0], line[1, 1])
    S1 = Segment(P1, P2)

    # triangle
    P3 = Point(points[p[0]][0], points[p[0]][1])
    P4 = Point(points[p[1]][0], points[p[1]][1])
    P5 = Point(points[p[2]][0], points[p[2]][1])

    S2 = Segment(P3, P4)
    S3 = Segment(P3, P5)
    S4 = Segment(P4, P5)

    M12 = S1.intersection(S2)
    M13 = S1.intersection(S3)
    M14 = S1.intersection(S4)

    C1 = S1.contains(P3)
    C2 = S1.contains(P4)
    C3 = S1.contains(P5)

    M = [M12, M13, M14]
    C = [C1 or C2, C1 or C3, C2 or C3]

    # 안에 있는 지 여부 확인
    cp1 = np.array(line[0, :])
    cp2 = np.array(line[1, :])
    p1 = points[p[0]]
    p2 = points[p[1]]
    p3 = points[p[2]]

    is_intersect = False
    for index in range(len(M)):
        if is_inside(cp1, p1, p2, p3) or is_inside(cp2, p1, p2, p3) or (len(M[index]) > 0 and not C[index]):
            result += [list(p)]
            break

result = np.array(result)
for point_index in result:
    p1, p2, p3 = point_index
    p1 = points[p1]
    p2 = points[p2]
    p3 = points[p3]
    triangle = np.array([p1, p2, p3])
    plt.fill(triangle[:, 0], triangle[:, 1], alpha=.3)

output = ""
for row in result:
    for item in row:
        output += str(item) + " "
    output += "\n"

file = open("points_out.txt", "w")
file.write(output)
file.close()

for i in range(len(line)):
    ptxt = str(i) + "(" + str(line[i][0]) + "," + str(line[i][1]) + ")"
    plt.annotate(ptxt, (line[i][0], line[i][1]), fontsize=9, fontweight='bold')
plt.plot(line[:, 0], line[:, 1], 'o')

plt.show()