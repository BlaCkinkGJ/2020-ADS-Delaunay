import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from sympy.geometry import *

OUTER = "outer [ ]"
FACE = "face [{},{},{}]"
VERTEX = "vertex [{}]"
EDGE = "edge [{},{}]"

vertexes = []
points = []

file = open("points.txt", "r")  # 파일 이름이 vertexes.txt입니다.
lines = file.readlines()
lines = [line.strip() for line in lines]
N = int(lines[0])
for index in range(1, N + 1):
    vertexes += [[int(item) for item in lines[index].split()]]
M = int(lines[N + 1])
for index in range(N + 2, N + M + 1 + 1):
    points += [[int(item) for item in lines[index].split()]]
file.close()

vertexes = np.array(vertexes)
points = np.array(points)

for i in range(len(vertexes)):
    ptxt = str(i) + "(" + str(vertexes[i][0]) + "," + str(vertexes[i][1]) + ")"
    plt.annotate(ptxt, (vertexes[i][0], vertexes[i][1]), fontsize=9, fontweight='bold')
plt.plot(vertexes[:, 0], vertexes[:, 1], 'o')

for i in range(len(points)):
    ptxt = str(i) + "(" + str(points[i][0]) + "," + str(points[i][1]) + ")"
    plt.annotate(ptxt, (points[i][0] - 0.25, points[i][1] - 0.4), fontsize=9, fontweight='bold', color='red')
plt.plot(points[:, 0], points[:, 1], 'o')


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

    if a1 == 0 or a2 == 0 or a3 == 0:
        return False

    if a == a1 + a2 + a3:
        return True
    else:
        return False


tri = Delaunay(vertexes)

plt.triplot(vertexes[:, 0], vertexes[:, 1], tri.simplices.copy())

result = []
for index in range(len(points)):
    command = OUTER
    for p in tri.simplices:
        # points
        CP = Point(points[index, 0], points[index, 1])

        # triangle
        P3 = Point(vertexes[p[0]][0], vertexes[p[0]][1])
        P4 = Point(vertexes[p[1]][0], vertexes[p[1]][1])
        P5 = Point(vertexes[p[2]][0], vertexes[p[2]][1])

        S2 = Segment(P3, P4)
        S3 = Segment(P3, P5)
        S4 = Segment(P4, P5)

        C1 = S2.contains(CP)
        C2 = S3.contains(CP)
        C3 = S4.contains(CP)

        # 안에 있는 지 여부 확인
        cp = np.array(points[index, :])
        p1 = vertexes[p[0]]
        p2 = vertexes[p[1]]
        p3 = vertexes[p[2]]

        if CP == P3:
            command = VERTEX.format(p[0])
            break
        elif CP == P4:
            command = VERTEX.format(p[1])
            break
        elif CP == P5:
            command = VERTEX.format(p[2])
            break

        if C1:
            command = EDGE.format(min(p[0], p[1]), max(p[0], p[1]))
            break
        elif C2:
            command = EDGE.format(min(p[0], p[2]), max(p[0], p[2]))
            break
        elif C3:
            command = EDGE.format(min(p[1], p[2]), max(p[1], p[2]))
            break

        if is_inside(cp, p1, p2, p3):
            command = FACE.format(p[0], p[1], p[2])
            break
    result += [command+'\n']

file = open("points_out.txt", "w")
file.writelines(result)
file.close()
plt.show()
