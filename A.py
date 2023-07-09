import cv2
import numpy as np
import threading
import colorsys
import heapq


class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x ** 2 + self.y ** 2) < (other.x ** 2 + other.y ** 2)


rw = 2
p = 0
start = Point()
end = Point()
dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]


def A_Star(s, e):
    global img, h, w
    const = 10000
    found = False
    heapq_l = []
    parent_d = {}
    parent_d[(s.x, s.y)] = None
    s_g, s_h = 0, abs(e.x - s.x) + abs(e.y + s.y)
    s_f = s_g + s_h
    heapq.heappush(heapq_l, (s_f, s))

    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    v[s.y][s.x] = 1
    while len(heapq_l) > 0:
        current_cell = heapq.heappop(heapq_l)[1]
        for d in dir4:
            cell = current_cell + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and
                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                cell_g, cell_h = abs(cell.x - s.x) + abs(cell.y - s.y), abs(cell.x - e.x) + abs(cell.y - e.y)
                cell_f = cell_g + cell_h
                heapq.heappush(heapq_l, (cell_f, cell))
                v[cell.y][cell.x] = v[current_cell.y][current_cell.x] + 1  # Later

                img[cell.y][cell.x] = list(reversed(
                    [i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)])
                )
                parent_d[(cell.x, cell.y)] = current_cell
                if cell == e:
                    found = True
                    ##                    del q[:]
                    break
    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent_d[(p.x, p.y)]
        path.append(p)
        path.reverse()

        for p in path:
            img[p.y][p.x] = [255, 255, 255]
        print("Path Found")
    else:
        print("Path Not Found")


def mouse_event(event, pX, pY, flags, param):
    global img, start, end, p

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(img, (pX - rw, pY - rw),
                          (pX + rw, pY + rw), (0, 0, 255), -1)
            start = Point(pX, pY)
            print("start = ", start.x, start.y)
            p += 1
        elif p == 1:
            cv2.rectangle(img, (pX - rw, pY - rw),
                          (pX + rw, pY + rw), (0, 200, 50), -1)
            end = Point(pX, pY)
            print("end = ", end.x, end.y)
            p += 1


def disp():
    global img
    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouse_event)
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(1)


img = cv2.imread("mazelevel.png", cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
h, w = img.shape[:2]
print("Select start and end points : ")
t = threading.Thread(target=disp, args=())
t.start()
while p < 2:
    pass
#BFS(start, end)
A_Star(start, end)
