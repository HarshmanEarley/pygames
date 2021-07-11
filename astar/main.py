import pygame
import math
from queue import PriorityQueue

#Window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algo")
FPS = 60

#Color
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128, 128, 128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (128, 0, 128)
TURQUOISE = (64, 122, 208)
ORANGE = (255,140,0)
TEAL = (0, 128, 128)

#GLOBALS
ROWS = 50


class node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == TEAL
    
    def reset(self):
        self.color = WHITE

    def set_start(self):
        self.color = ORANGE

    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN
    
    def set_wall(self):
        self.color = BLACK

    def set_start(self):
        self.color = BLUE

    def set_end(self):
        self.color = TEAL

    def set_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        self.neighbours = []

        if self.row < self.total_rows - 1 and not grid[self.row - 1][self.col].is_wall(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])            

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])        

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # RIGHT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# Huristic, calc manhatten distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(node(i, j, gap, rows))
    return grid

def draw_grid(win, rows, width):
   gap = width // rows
   for i in range(rows): #horizontal
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) 
        for j in range(rows): #vertical
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))   

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win) 
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap

    return row, col 

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()

def algo(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row} # Keeps track of current shortest distance from start node to this node
    g_score[start] = 0 
    f_score = {spot: float("inf") for row in grid for spot in row} # Keeps track of predicted distance from this node to end
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # Hit the end node, finalise path
            reconstruct_path(came_from, end, draw)
            end.set_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.set_open()

        draw()

        if current != start:
            current.set_closed()


def main(win, width):
    rows = ROWS
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        #draw to screen
        draw(win, grid, rows, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            
            #left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.set_start()

                elif not end and node != start:
                    end = node
                    end.set_end()

                elif node != end and node != start:
                    node.set_wall()
                
            #Right mouse button
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_c: # Clear all    
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                            
                if event.key == pygame.K_SPACE and start and end: # Start Algo
                    # Need both start and end to run
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algo(lambda: draw(win, grid, ROWS, width), grid, start, end)



    pygame.quit()

main(WIN,WIDTH)