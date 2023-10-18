import turtle as tu
import math as m
import itertools as tool
from tkinter import messagebox

#Paramètrage de Turtle (Force FullScreen + Instant Update) + Variable de l'état du jeu
tu.Screen().setup(width = 1.0, height = 1.0)
tu.Screen().getcanvas().winfo_toplevel().overrideredirect(1)
tu.Screen().tracer(0)
loop_started = False
mouse_x, mouse_y = 0, 0

#Message au lancement du jeu
messagebox.showinfo("The Game Of Life", "1 - Change the state of the cells by clicking on them\n2 - Start the simulation by pressing SPACE\n3 - End the fun by pressing SPACE again\n\nWarning ! The game has freezing issues !") # The alert.


class Pixel(tu.Turtle):

    def __init__(self, coords, pixel_state, dead_neig, alive_neig):
        super().__init__(visible = False)  
        self.coords = coords
        self.coords[0], self.coords[1] = self.coords[0], self.coords[1]
        self.pixel_state = pixel_state
        self.dead_neig = dead_neig
        self.alive_neig = alive_neig

    #Fonction qui compte le nombre de cellules voisines mortes et vivante
    def neig_state(self):
        self.dead_neig = 0
        self.alive_neig = 0
        for x_n, y_n in tool.product(range(3),range(3)):
            if state_list[self.coords[1]+y_n-1][self.coords[0]+x_n-1] == 0:
                self.dead_neig += 1
        if state_list[self.coords[1]][self.coords[0]] == 0:
            self.dead_neig += -1
        self.alive_neig = 8-self.dead_neig

    #Fonction qui change l'état de la celulle en fonction de ses voisins.
    def change_pixel_state(self):
        if self.pixel_state == 0 and self.alive_neig == 3:
            self.pixel_state = 1
        elif self.pixel_state == 1 and self.alive_neig not in [2,3]:
            self.pixel_state = 0
            
    def clear_pixel(self):
        self.clear()

    #Fonction qui dessine la cellule 
    def draw_pixel(self):
        self.up()
        self.goto(self.coords[0]*10-tu.window_width()/2, self.coords[1]*10-tu.window_height()/2)
        self.seth(0)
        self.down()
        self.color('black')
        self.begin_fill()
        for i in range(4):
            self.seth(i*90)
            self.forward(10)
        self.end_fill()

    def tick(self):
        global loop_started
        self.clear()
        if loop_started == True:
            loop()
        else:
            tu.register_shape('10_10_square', ((0, 0), (0, 10), (10, 10), (10, 0)))
            self.shape("10_10_square")
            self.color('red')
            self.goto(m.floor(mouse_x/10)*10, m.floor((mouse_y)/10)*10+10)
            self.stamp()
            tu.Screen().ontimer(self.tick, 1000 // 30)

#Fonction qui calcul les coordonées du curseur
def on_motion(event):
    global mouse_x, mouse_y, loop_started
    if loop_started == False:
        mouse_x = event.x - tu.window_width() / 2
        mouse_y = -event.y + tu.window_height() / 2

#Fonction qui change les états des cellules lors d'un clic.
def on_click_change(x,y):
    state_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)] += 1
    object_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)].pixel_state += 1
    if state_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)] == 2:
        state_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)] = 0
        object_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)].pixel_state = 0
        object_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)].clear_pixel()
    else:
        object_list[int((y+tu.window_height()/2)/10)][int((x+tu.window_width()/2)/10)].draw_pixel()
    tu.Screen().update()

def loop():
    global loop_started
    generation_number = 0
    twrite = tu.Turtle(visible = False)
    loop_started = True
    tu.listen()
    while True:
        for x, y in tool.product(range(int(tu.window_width()/10)), range(int(tu.window_height()/10))):
            object_list[y+1][x+1].neig_state()
            object_list[y+1][x+1].change_pixel_state()
            if object_list[y+1][x+1].pixel_state == 1:
                object_list[y+1][x+1].draw_pixel()
            else:
                object_list[y+1][x+1].clear_pixel()
        for x, y in tool.product(range(int(tu.window_width()/10)), range(int(tu.window_height()/10))):
            state_list[y+1][x+1] = object_list[y+1][x+1].pixel_state
        generation_number += 1
        twrite.goto(0, 0)
        twrite.clear()
        print(generation_number)
        twrite.write(f'Generation number : {generation_number}', False, align = 'left', font=('Arial', 50, 'normal'))
        tu.Screen().update()
        tu.onkeypress(exit_func, 'space')
        tu.Screen().update()

def exit_func():
    tu.bye()
    exit()


tick_object = Pixel([-1,-1], 0, 0, 0)

#Création du tableau de jeu
state_list = [[0 for x in range(int(tu.window_width()/10)+2)] for y in range(int(tu.window_height()/10)+2)]
object_list = [[(Pixel([x,y], state_list[y][x], 0, 0)) for x in range(int(tu.window_width()/10)+2)] for y in range(int(tu.window_height()/10)+2)]

tu.listen()
tu.Screen().onclick(on_click_change)
tu.onkeypress(loop, 'space') #Appelle la fonction Loop lorsque l'utilisateur appuie sur Espace
tu.getcanvas().bind("<Motion>", on_motion)#Appelle la fonction on_motion lorsque l'utilisateur bouge le curseur de la souris
tick_object.tick()
tu.Screen().mainloop()
