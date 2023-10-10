import turtle as tu
import math as m
import itertools as tool
import time as ti

tu.Screen().tracer(0)
state_list = [[0 for x in range(int(tu.screensize()[0]/10)+2)] for y in range(int(tu.screensize()[1]/10)+2)]

def on_click_change(x,y):
    state_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)] += 1
    if state_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)] == 1:
        state_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)] = 0
    
def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x - tu.window_width() / 2
    mouse_y = -event.y + tu.window_height() / 2

def tick():
    tu.clear()
    tu.goto(m.floor(mouse_x/10)*10, m.floor(mouse_y/10)*10)
    tu.stamp()
    tu.Screen().ontimer(tick, 1000 // 30)
    
class Pixel(tu.Turtle):

    def __init__(self, coords, pixel_state, dead_neig, alive_neig):
        super().__init__(visible = False)  
        self.coords = coords
        self.coords[0], self.coords[1] = self.coords[0], self.coords[1]
        self.pixel_state = pixel_state
        self.dead_neig = dead_neig
        self.alive_neig = alive_neig

    def neig_state(self):
        self.dead_neig = 0
        self.alive_neig = 0
        for x_n, y_n in tool.product(range(3),range(3)):
            if state_list[self.coords[1]+y_n-1][self.coords[0]+x_n-1] == 0:
                self.dead_neig += 1
        if state_list[self.coords[1]][self.coords[0]] == 0:
            self.dead_neig += -1
        self.alive_neig = 8-self.dead_neig

    def change_pixel_state(self):
        if self.pixel_state == 0 and self.alive_neig == 3:
            self.pixel_state = 1
        elif self.pixel_state == 1 and self.alive_neig not in [2,3]:
            self.pixel_state = 0
            
    def clear_pixel(self):
        self.clear()

    def draw_pixel(self):
        self.up()
        self.goto(self.coords[0]*10,self.coords[1]*10)
        self.seth(0)
        self.begin_fill()
        self.down()
        for i in range(4):
            self.seth(i*90)
            self.forward(10)
        self.end_fill()

tu.Screen().onclick(on_click_change)
mouse_x, mouse_y = 0, 0
tu.getcanvas().bind("<Motion>", on_motion)
tu.register_shape('10_10_square', ((0, 0), (0, 10), (10, 10), (10, 0)))
tu.shape("10_10_square")
tu.color('red')
tu.up()
tick()
tu.Screen().mainloop()


object_list = [[(Pixel([x,y], state_list[y][x], 0, 0)) for x in range(int(tu.screensize()[0]/10)+2)] for y in range(int(tu.screensize()[1]/10)+2)]

while True:
    for x, y in tool.product(range(int(tu.screensize()[0]/10)), range(int(tu.screensize()[1]/10))):
        object_list[y+1][x+1].neig_state()
        object_list[y+1][x+1].change_pixel_state()
        if object_list[y+1][x+1].pixel_state == 1:
            object_list[y+1][x+1].draw_pixel()
        else:
            object_list[y+1][x+1].clear_pixel()
    for x, y in tool.product(range(int(tu.screensize()[0]/10)), range(int(tu.screensize()[1]/10))):
        state_list[y+1][x+1] = object_list[y+1][x+1].pixel_state
    tu.Screen().update()
    ti.sleep(0.1)

tu.exitonclick()
