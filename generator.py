import random

MAX_SIZE = 50
MAX_X = 50
MAX_Y = 50

file = open("points4.txt", "w")

for i in range(2):
    N = random.randint(MAX_SIZE // ((i + 1) * 2), MAX_SIZE // (i + 1))

    point_set = set()
    for _ in range(N):
        x = random.randint(0, MAX_X)
        y = random.randint(0, MAX_Y)
        point_set.add((x, y))

    N = len(point_set)
    file.write("{}\n".format(N))
    for x, y in point_set:
        file.write("{} {}\n".format(x, y))

file.close()
