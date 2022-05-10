import gzip
from statistics import median
import collections
import operator
import sys
import requests
import datetime


searchOption = str(sys.argv[1])
database = str(sys.argv[2])
queries = str(sys.argv[3])
indexBlock = " "
if len(sys.argv) == 5:
    indexBlock = sys.argv[4]

# with gzip.open('projDB.gz', 'rb') as f_in:
#    with open('file.txt', 'wb') as f_out:
#        shutil.copyfileobj(f_in, f_out)

#url = "https://www.cise.ufl.edu/~tamer/teaching/spring2022/other/test6"
#filename = url.split("/")[-1]
# with open(filename, "wb") as f:
#    r = requests.get(url)
#    f.write(r.content)

data = []

with open(database, "r") as f:  # opens the file in read mode
    for line in f:   # puts the file into an array
        currentline = line.split(",")
        entry = []
        for i in range(len(currentline)):
            entry.append(int(currentline[i]))
        data.append(entry)


def sequential(data):
    with open(queries, "r") as filestream:  # 'projquery'
        with open('sequentialOutput.txt', 'w') as f:
            for line in filestream:
                if line == "\n":
                    continue
                temp = []
                # print(line)
                f.write(line + '\n')
                currentline = line.split(" ")
                xmin = int(currentline[0])
                xmax = int(currentline[1])
                ymin = int(currentline[2])
                ymax = int(currentline[3])

                for d in data:
                    if xmin <= d[0] and d[0] <= xmax and ymin <= d[1] and d[1] <= ymax:
                        # print(d)
                        temp.append(d)
                temp.sort(key=lambda y: (y[0], y[1]))
                for i in temp:
                    f.write(str(i) + '\n')
                f.write('\n')
        f.close()


BT = collections.namedtuple("BT", ["D", "value", "left", "right"])


def kdTree(points):
    k = len(points[0])
    flag = True

    def build(*, points, depth, flag):
        if len(points) == 0:
            return None

        points.sort(key=operator.itemgetter(depth % k))
        # print(points)
        middle = len(points) // 2

        temp = []
        dimension = " "
        for p in points:
            if flag:
                flag = False
                break
            if p[depth % k] == points[middle][depth % k]:
                # print(points[middle])
                temp.append(p)
            if len(temp) == int(indexBlock):
                break
        if depth % k == 0:
            dimension = "X: "
        else:
            dimension = "Y: "

        return BT(
            D=dimension + str(points[middle][depth % k]),
            value=temp,
            left=build(
                points=points[:middle],
                depth=depth+1,
                flag=flag
            ),
            right=build(
                points=points[middle+1:],
                depth=depth+1,
                flag=flag
            ),
        )

    return build(points=list(points), depth=0, flag=flag)


def kdTreeSearch(*, tree):
    k = 2

    flag = True
    file = open('kdTreeOutput.txt', 'w')

    def search(*, tree, depth, flag, temp):
        if tree is None:
            return

        for i in range(len(tree.value)):
            if xmin <= tree.value[i][0] and tree.value[i][0] <= xmax and ymin <= tree.value[i][1] and tree.value[i][1] <= ymax:
                # print(tree.value[i])
                temp.append(tree.value[i])

        axis = depth % k

        if flag:
            flag = False
            search(tree=tree.right, depth=depth+1, flag=flag, temp=temp)
            search(tree=tree.left, depth=depth+1, flag=flag, temp=temp)
        elif axis == 0 and tree.value[0][axis] < xmin:
            search(tree=tree.right, depth=depth+1, flag=flag, temp=temp)
        elif axis == 0 and tree.value[0][axis] > xmax:
            search(tree=tree.left, depth=depth+1, flag=flag, temp=temp)
        elif axis == 1 and tree.value[0][axis] < ymin:
            search(tree=tree.right, depth=depth+1, flag=flag, temp=temp)
        elif axis == 1 and tree.value[0][axis] > ymax:
            search(tree=tree.left, depth=depth+1, flag=flag, temp=temp)
        else:
            search(tree=tree.right, depth=depth+1, flag=flag, temp=temp)
            search(tree=tree.left, depth=depth+1, flag=flag, temp=temp)

    with open(queries, "r") as filestream:
        for line in filestream:
            if line == "\n":
                continue
            temp = []
            # print(line)
            file.write(line + '\n')
            currentline = line.split(" ")
            xmin = int(currentline[0])
            xmax = int(currentline[1])
            ymin = int(currentline[2])
            ymax = int(currentline[3])

            search(tree=tree, depth=0, flag=flag, temp=temp)
            temp.sort(key=lambda y: (y[0], y[1]))
            for i in temp:
                file.write(str(i) + '\n')
            file.write('\n')
    file.close()


def MYkdTree(points):

    k = len(points[0])

    def build(*, points, depth):
        if len(points) == 0:
            return None

        points.sort(key=operator.itemgetter(depth % k))
        middle = len(points) // 2

        if depth % k == 0:
            dimension = "X: "
        else:
            dimension = "Y: "

        return BT(
            D=dimension + str(points[middle][depth % k]),
            value=points[middle],
            left=build(
                points=points[:middle],
                depth=depth+1,
            ),
            right=build(
                points=points[middle+1:],
                depth=depth+1,
            ),
        )

    return build(points=list(points), depth=0)


def MYkdTreeSearch(*, tree):
    k = 2
    file1 = open('MykdTreeOutput.txt', 'w')

    def search(*, tree, depth, temp):
        if tree is None:
            return

        if xmin <= tree.value[0] and tree.value[0] <= xmax and ymin <= tree.value[1] and tree.value[1] <= ymax:
            # print(tree.value)
            temp.append(tree.value)

        axis = depth % k

        if axis == 0 and tree.value[axis] < xmin:
            search(tree=tree.right, depth=depth+1, temp=temp)
        elif axis == 0 and tree.value[axis] > xmax:
            search(tree=tree.left, depth=depth+1, temp=temp)
        elif axis == 1 and tree.value[axis] < ymin:
            search(tree=tree.right, depth=depth+1, temp=temp)
        elif axis == 1 and tree.value[axis] > ymax:
            search(tree=tree.left, depth=depth+1, temp=temp)
        else:
            search(tree=tree.right, depth=depth+1, temp=temp)
            search(tree=tree.left, depth=depth+1, temp=temp)

    with open(queries, "r") as filestream:
        for line in filestream:
            if line == "\n":
                continue
            temp = []
            # print(line)
            file1.write(line + '\n')
            currentline = line.split(" ")
            xmin = int(currentline[0])
            xmax = int(currentline[1])
            ymin = int(currentline[2])
            ymax = int(currentline[3])

            search(tree=tree, depth=0, temp=temp)
            temp.sort(key=lambda y: (y[0], y[1]))
            for i in temp:
                file1.write(str(i) + '\n')
            file1.write('\n')
    file1.close()


if searchOption == "0":
    start = datetime.datetime.now()
    print(start)
    sequential(data)
    end = datetime.datetime.now()
    print(end)
    c = end - start
    print(c.seconds)
elif searchOption == "1":
    tree = kdTree(data)
    start = datetime.datetime.now()
    print(start)
    kdTreeSearch(tree=tree)
    end = datetime.datetime.now()
    print(end)
    c = end - start
    print(c.seconds)
elif searchOption == "2":
    tree = MYkdTree(data)
    start = datetime.datetime.now()
    print(start)
    MYkdTreeSearch(tree=tree)
    end = datetime.datetime.now()
    print(end)
    c = end - start
    print(c.seconds)
