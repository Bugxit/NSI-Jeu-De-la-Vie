import turtle as tu
import itertools as tool

tu.Screen().tracer(0)
state_list = [0 for y in range(int((tu.screensize()[0]*tu.screensize()[1])/100))]
object_list = []

class Pixel():

    def __init__(self, coords, pixel_state, dead_neig, alive_neig):
        self.coords = coords
        self.pixel_state = pixel_state
        self.dead_neig = dead_neig
        self.alive_neig = alive_neig

    def neig_state(self):
        for x_n, y_n in tool.product(range(3),range(3)):
            if state_list[int((self.coords[0]+x_n-1)+(self.coords[1]+y_n-1)*(tu.screensize()[0]/10))] == 0:
                self.dead_neig += 1
        if state_list[int((self.coords[0])+(self.coords[1])*(tu.screensize()[0]/10))] == 0:
            self.dead_neig -=1
        self.alive_neig = 8-self.dead_neig

    def change_pixel_state(self):
        if self.pixel_state == 0 and self.alive_neig == 3:
            self.pixel_state = 1
        elif self.pixel_state == 1 and self.alive_neig not in [2,3]:
            self.pixel_state = 0

    def pixel(self):
        tu.up()
        tu.goto(self.coords[0]*10,self.coords[1]*10)
        tu.seth(0)
        tu.begin_fill()
        for i in range(4):
            tu.seth(i*90)
            tu.forward(10)
        tu.end_fill()

for x, y in tool.product(range(int(tu.screensize()[0]/10)), range(int(tu.screensize()[1]/10))):
    object_list.append(Pixel((x,y), 0, 0, 0))

while True:
    for i in range(len(object_list)):
        object_list[i].neig_state()
        object_list[i].change_pixel_state()
        if object_list[i].pixel_state == 1:
            object_list[i].pixel()
    tu.Screen().update()

