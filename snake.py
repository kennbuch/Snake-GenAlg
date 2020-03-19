
class Cube:

    def __init__(self, pos, dirx=0, diry=0):
        self.pos = pos      # position of the cube
        self.dirx = dirx    # x direction the cube is moving
        self.diry = diry    # y direction the cube is moving


    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)


class Snake:

    def __init__(self, x, y):       
        self.x = x                  # width of the board
        self.y = y                  # height of the board
        self.dirx = 1               # x direction the snake is moving
        self.diry = 0               # y direction the snake is moving
        self.head = Cube((int(self.x/2), int(self.y/2)),
                          self.dirx, self.diry)  # head of the snake 

        self.body = [self.head]     # list of Cubes that make up the snake
        self.turns = {}             # dictionary of positions that indicate a turn in the snake's body


    def move(self, dir):
        if dir == "up":
            # if head crashes into a wall return false
            if self.head.pos[1] <= 0:
                return False
            # change the direction the snake is moving 
            self.dirx = 0  
            self.diry = -1
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]
        elif dir == "down":
            if self.head.pos[1] >= self.y - 1:
                return False
            self.dirx = 0
            self.diry = 1
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]
        elif dir == "left":
            if self.head.pos[0] <= 0:
                return False
            self.dirx = -1
            self.diry = 0
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]
        elif dir == "right":
            if self.head.pos[0] >= self.x - 1:
                return False
            self.dirx = 1
            self.diry = 0
            self.turns[self.head.pos[:]] = [self.dirx, self.diry]
        else: 
            if self.head.pos[1] + self.diry < 0 or self.head.pos[1] + self.diry >= self.y or\
               self.head.pos[0] + self.dirx < 0 or self.head.pos[0] + self.dirx >= self.x:
                return False
        
        # check if the snake ran into its own body
        for i in range(len(self.body)):
            if self.body[i].pos in list(map(lambda z:z.pos, self.body[i + 1:])):
                return False

        for i, c in enumerate(self.body):
            p = c.pos[:]

            # if there is a turn at this position change the direction of the cube
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # if this is the last cube of this turn delete the turn
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            # else continue in the same direction
            else:
                c.move(c.dirx, c.diry)

        return True

    def grow(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        # append the body in the direction opposite the tail is moving
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]), dx, dy))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), dx, dy))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), dx, dy))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), dx, dy))


    def reset(self):
        self.dirx = 1
        self.diry = 0
        self.head = Cube((int(self.x/2), int(self.y/2)), self.dirx, self.diry)
        self.body = [self.head]
        self.turns = {}

    def distance_to_food(self, food):
        return abs(self.head.pos[0] - food.pos[0]) + abs(self.head.pos[1] - food.pos[1])


    def get_NN_input(self, food):
        x = []
        
        x.extend(self.look_in_direction(food, 0, -1))  # look for objects in the N direction
        x.extend(self.look_in_direction(food, 1, -1))  # look for objects in the NE direction
        x.extend(self.look_in_direction(food, 1, 0))   # look for objects in the E direction
        x.extend(self.look_in_direction(food, 1, 1))   # look for objects in the SE direction
        x.extend(self.look_in_direction(food, 0, 1))   # look for objects in the S direction
        x.extend(self.look_in_direction(food, -1, 1))  # look for objects in the SW direction
        x.extend(self.look_in_direction(food, -1, 0))  # look for objects in the W direction
        x.extend(self.look_in_direction(food, -1, -1)) # look for objects in the NW direction
        
        return x
    
    def look_in_direction(self, food, dirx, diry):

        x = [0, 0, 0]
    
        wall_x = 0 if dirx == -1 else self.x # x position of the wall in the direction the snake is looking
        wall_y = 0 if diry == -1 else self.y # y position of the wall in the direction the snake is looking
        
        i = 0
        found_food = False
        found_body = False
        new_pos = [self.head.pos[0], self.head.pos[1]]

        while True:
            # break out of loop if we hit the wall 
            if new_pos[0] == wall_x or new_pos[1] == wall_y:
                break
            
            # mark the distance to the food if it is in the direction the snake is looking 
            if (not found_food and tuple(new_pos) == food.pos):
                x[0] = 1 - (i / self.x)
                found_food = True
            
            # mark the distance of the first body part in the direction the snake is looking
            if (not found_body and tuple(new_pos) in [body.pos for body in self.body]):
                x[1] = 1 - (i / self.x)
                found_body = True

            new_pos[0] += dirx
            new_pos[1] += diry
            i += 1
        
        # mark the distance to the wall in the direction the snake is looking 
        x[2] = 1 - (i / self.x)

        return x
