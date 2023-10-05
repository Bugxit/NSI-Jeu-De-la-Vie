import turtle as tu
import itertools as tool
import time as ti

tu.Screen().tracer(0)
state_list = [[0 for x in range(int(tu.screensize()[0]/10)+1)] for y in range(int(tu.screensize()[1]/10)+1)]

class Pixel():

    def __init__(self, coords, pixel_state, dead_neig, alive_neig):
        self.coords = coords
        self.coords[0], self.coords[1] = self.coords[0]-1, self.coords[1]-1
        self.pixel_state = pixel_state
        self.dead_neig = dead_neig
        self.alive_neig = alive_neig

    def neig_state(self):
        self.dead_neig = 0
        self.alive_neig = 0
        for x_n, y_n in tool.product(range(3),range(3)):
            if state_list[self.coords[1]+y_n-1][self.coords[0]+x_n-1] == 0:
                self.dead_neig += 1
        if state_list[self.coords[1]+y_n-1][self.coords[0]+x_n-1]== 0:
            self.dead_neig -=1
        self.alive_neig = 8-self.dead_neig

    def change_pixel_state(self):
        if self.pixel_state == 0 and self.alive_neig == 3:
            self.pixel_state = 1
        elif self.pixel_state == 1 and self.alive_neig not in [2,3]:
            self.pixel_state = 0

    def draw_pixel(self):
        tu.up()
        tu.goto(self.coords[0]*10,self.coords[1]*10)
        tu.seth(0)
        tu.begin_fill()
        for i in range(4):
            tu.seth(i*90)
            tu.forward(10)
        tu.end_fill()

state_list[10][9] = 1
state_list[10][10] = 1
state_list[10][11] = 1

while True:
    object_list = [[(Pixel([x,y], state_list[y][x], 0, 0)) for x in range(int(tu.screensize()[0]/10)+1)] for y in range(int(tu.screensize()[1]/10)+1)]
    for x, y in tool.product(range(int(tu.screensize()[0]/10)+1), range(int(tu.screensize()[1]/10)+1)):
        state_list[y][x] = object_list[y][x].pixel_state
    for x, y in tool.product(range(int(tu.screensize()[0]/10)+1), range(int(tu.screensize()[1]/10)+1)):
        object_list[y][x].neig_state()
        object_list[y][x].change_pixel_state()
        if object_list[y][x].pixel_state == 1:
            object_list[y][x].draw_pixel()
        state_list = []
    tu.Screen().update()
    ti.sleep(1)
