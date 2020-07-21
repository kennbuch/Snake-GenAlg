import tkinter as tk 
import tkinter.messagebox as mb
import numpy as np
from snake import Snake, Cube
from time import sleep
from random import randrange

def draw_board(canv, rows): 
    width = canv.winfo_width()
    space = width / rows
    x = 0
    for _ in range(rows):
        x += space
        canv.create_line(x, 0, x, width, fill="white")
        canv.create_line(0, x, width, x, fill="white")

def draw_snake(canv, rows, snake):
    size = canv.winfo_width() / rows

    for i, c in enumerate(snake.body):
        canv.create_rectangle(c.pos[0]*size, c.pos[1]*size, (c.pos[0] + 1)*size, (c.pos[1] + 1)*size, fill="red")
        if i == 0:
            canv.create_oval(c.pos[0]*size + size/2 + 6, c.pos[1]*size + size/2 + 6, c.pos[0]*size + size/2 + 2, c.pos[1]*size + size/2 + 2, fill="black")
            canv.create_oval(c.pos[0]*size + size/2 + 6, c.pos[1]*size + size/2 - 6, c.pos[0]*size + size/2 + 2, c.pos[1]*size + size/2 - 2, fill="black")

def draw_food(canv, rows, food):
    size = canv.winfo_width() / rows
    canv.create_rectangle(food.pos[0]*size, food.pos[1]*size, (food.pos[0] + 1)*size, (food.pos[1] + 1)*size, fill="green")

def redrawWindow(canvas, rows, snake, food):
    canvas.delete('all')
    #draw_board(canvas, rows)
    draw_snake(canvas, rows, snake)
    draw_food(canvas, rows, food)
    canvas.update()

def get_move(event):
    key = event.keysym
    if key == 'w' or key == 'Up':
        snake.move('up')
    elif key == 's' or key == 'Down':
        snake.move('down')
    elif key == 'a' or key == 'Left':
        snake.move('left')
    elif key == 'd' or key == 'Right':
        snake.move('right')

def randomFood(rows, snake):
    positions = snake.body

    while True:
        x = randrange(rows)
        y = randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    
    return (x, y)

def visual(brain=None, human_player=True):
    global root
    root = tk.Tk()

    bg = "#2b2b2b"

    root.configure(background=bg)                          
    root.geometry("640x480")                                
    root.resizable(False, False)
    if human_player:
        root.bind("<KeyPress>", get_move)
    root.update()

    title = tk.Label(root, text="", bg=bg, fg="red", font=("Arial bold", 5))
    title.pack(side=tk.TOP)
    title.update()


    canv = tk.Canvas(root, width=470-title.winfo_height(), height=470-title.winfo_height(), bg=bg)
    canv.pack(side=tk.TOP)
    canv.update()

    rows = 20

    global snake 
    snake = Snake(rows, rows)
    
    food = Cube(randomFood(rows, snake))
    directions = ['up', 'down', 'left', 'right']
    hunger = 0
    while(True):
        sleep(0.02)
        direction = ''
        
        if not human_player:
            x = np.array([snake.get_NN_input(food)])
            y = brain.predict(x, get_index=True)
            direction = directions[y]

        if not snake.move(direction) or hunger == 150:
            answer = mb.askyesno("Game Over", "Score: " + str(len(snake.body)) + "\nWould you like to retry?")
            if answer == True:
                snake.reset()
                food = Cube(randomFood(rows, snake))
                hunger = 0
            else:
                root.destroy()
                break

        if snake.head.pos == food.pos:
            snake.grow()
            food = Cube(randomFood(rows, snake))
            hunger = 0
        else:
            hunger += 1


        redrawWindow(canv, rows, snake, food)

    root.mainloop()