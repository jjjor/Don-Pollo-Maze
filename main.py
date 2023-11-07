import pygame
from random import choice
from stack import Stack

RES = WIDTH, HEIGHT = 800, 600
TILE = 50
cols, rows, = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'bottom': True, 'right': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('grey'), (x + 2, y + 2, TILE - 2, TILE - 2))

    # def draw(self):
    #     x, y = self.x * TILE, self.y * TILE
    #     if self.visited:
    #         pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

    #     if self.walls['top']:
    #         pygame.draw.line(sc, pygame.Color('blue'), (x, y), (x + TILE, y), 2)
    #     if self.walls['right']:
    #         pygame.draw.line(sc, pygame.Color('blue'), (x + TILE, y), (x + TILE, y + TILE), 2)
    #     if self.walls['bottom']:
    #         pygame.draw.line(sc, pygame.Color('blue'), (x + TILE, y + TILE), (x, y + TILE), 2)
    #     if self.walls['left']:
    #         pygame.draw.line(sc, pygame.Color('blue'), (x, y + TILE), (x, y), 2)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell (self.x - 1, self.y)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    # Função para calcular a direção da célula em relação à saída
def direction_to_exit(self, exit_cell):
    dx = self.x - exit_cell.x
    dy = self.y - exit_cell.y

    if dx == 1:
        return 'left'
    elif dx == -1:
        return 'right'
    elif dy == 1:
        return 'top'
    elif dy == -1:
        return 'bottom'
    
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def load_maze_from_file(filename):
    with open(filename, "r") as file:
        maze_text = file.read()

    maze_lines = maze_text.split("\n")
    maze_cells = [list(line) for line in maze_lines if line]

    return maze_cells

maze_cells = load_maze_from_file("labirinto.txt")

def draw_maze(maze_cells):
    for y, row in enumerate(maze_cells):
        for x, cell in enumerate(row):
            if cell == "0":
                pygame.draw.line(sc, pygame.Color('blue'), (x * TILE, y * TILE), (x * TILE + TILE, y * TILE), 2)
                pygame.draw.line(sc, pygame.Color('blue'), (x * TILE + TILE, y * TILE), (x * TILE + TILE, y * TILE + TILE), 2)
                pygame.draw.line(sc, pygame.Color('blue'), (x * TILE + TILE, y * TILE + TILE), (x * TILE, y * TILE + TILE), 2)
                pygame.draw.line(sc, pygame.Color('blue'), (x * TILE, y * TILE + TILE), (x * TILE, y * TILE), 2)
            elif cell == "0":
                pygame.draw.line(sc, pygame.Color('blue'), (x * TILE, y * TILE), (x * TILE, y * TILE + TILE), 2)
            elif cell == "1":
                pygame.draw.line(sc, pygame.Color('blue'), (x * TILE, y * TILE), (x * TILE + TILE, y * TILE), 2)

maze_cells = load_maze_from_file("labirinto.txt")
    
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = [Stack]

while True:
    
    sc.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    draw_maze(maze_cells)

    #[cell.draw() for cell in grid_cells]
    current_cell.visited = True
    #current_cell.draw_current_cell()

    exit_cell = grid_cells[-1]
    if current_cell == exit_cell:
        
        break

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    x, y = exit_cell.x * TILE, exit_cell.y * TILE
    pygame.draw.rect(sc, pygame.Color('green'), (x + 2, y + 2, TILE - 2, TILE - 2))
    pygame.display.flip()

    pygame.display.flip()
    clock.tick(30)


# Exibir a mensagem
sc.fill(pygame.Color('black'))
font = pygame.font.Font(None, 36)
text = font.render("GUSTAVO É VIADO", True, pygame.Color('white'))
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
sc.blit(text, text_rect)
pygame.display.flip()

# Aguardar um tempo antes de fechar a janela (por exemplo, 3 segundos)
pygame.time.delay(3000)

# Encerrar o jogo
pygame.quit()

    

