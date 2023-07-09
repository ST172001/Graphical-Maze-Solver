import cv2
import numpy as np
import threading

######
#THIS PROGRAM CONTAINS BOTH DFS AND BFS
#TO USE DFS JUST COMMENT BFS AND VICEVERSA AT THE END OF PROGRAM


#CREATED A CLASS POINT AND USED OPERATOR OVERLOADING
class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


#initialize the variables
p = 0
c=0
start = Point()
end = Point()
dir4 = [Point(1,0 ), Point(0, 1), Point(0,-1), Point(-1, 0)]

#BFS:TO USE BFS COMMENT DFS AT THE END OF PROGRAM
def BFS(s, e):
    global img, h, w,c
    solved = False
    queue= []
    visited = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    queue.append(s)
    visited[s.y][s.x] = 1
    while len(queue) > 0:
        p = queue.pop(0)
        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and visited[cell.y][cell.x] == 0 and
                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                queue.append(cell)
                visited[cell.y][cell.x] = 1
                img[cell.y][cell.x] = (40,40,40)
                parent[cell.y][cell.x] = p
                if cell == e:
                    solved = True
                    del queue[:]
                    break
    path = []
    if solved:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()

        for p in path:
            img[p.y][p.x] = [255, 255, 255]
            c+=1
        print("BFS")
        print("Path Found")
        print("Path length is:",c)
    else:
        print("Path Not Found")

#DFS:TO USE DFS COMMENT BFS AT THE END OF PROGRAM
def DFS(s, e):
    global img, h, w,c
    const = 10000
    found = False
    q = []
    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    q.append(s)
    v[s.y][s.x] = 1
    while len(q) > 0:
        p = q.pop()
        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and
                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                q.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later

                img[cell.y][cell.x] =(40,40,40)
                parent[cell.y][cell.x] = p
                if cell == e:
                    found = True
                    del q[:]
                    break
    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()

        for p in path:
            img[p.y][p.x] = [255, 255, 255]
            c+=1
        print("DFS")
        print("Path Found")
        print("Path Length:",c)
    else:
        print("Path Not Found")


def mouse_event(event, pX, pY, flags, param):
    global img, start, end, p

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.circle(img,(pX,pY),2,(0,0,255),2)
            start = Point(pX, pY)
            print("start = ", start.x, start.y)
            p += 1
        elif p == 1:
            cv2.circle(img, (pX, pY), 2, (0, 255, 0),2)
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


#COMMENT THE TYPE OF METHOD YOU DONT WANT TO SEE
#CURRENTLY IT DISPLAYS BFS ON THE SCREEN
BFS(start, end)
#DFS(start, end)

