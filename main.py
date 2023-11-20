import pygame
import time
from collections import deque

pygame.init()
pygame.mixer.init()
victory_royale = pygame.mixer.Sound('sounds/victory_royale.wav')
som_reproduzido = False

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def load_maze_from_file(filename):
    maze = []
    positionRX, positionRY = 0, 0
    positionCX, positionCY = 0, 0

    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            row = []
            for j, char in enumerate(line.strip()):
                if char == '0':
                    row.append(0)
                elif char == '1':
                    row.append(1)
                elif char == 'm':
                    row.append(2)
                    positionRX, positionRY = j, i
                elif char == 'c':
                    row.append(3)
                    positionCX, positionCY = j, i
            maze.append(row)
    h = len(maze)
    w = len(maze[0])
    return maze, h, w, positionRX, positionRY, positionCX, positionCY

maze, h, w, positionRX, positionRY, positionCX, positionCY = load_maze_from_file('labirintoteste.txt')

cell_size = min(1200 // w, 720 // h)
width = w * cell_size
height = h * cell_size

pygame.display.set_caption('RUN FOR THE SCARLORD')

size = (width, height)
screen = pygame.display.set_mode(size)

largura_imagem = 200
altura_imagem = 100
imagem_fim_jogo = pygame.image.load("imgs/vitoria.png")
imagem_fim_jogo = pygame.transform.scale(imagem_fim_jogo, (largura_imagem, altura_imagem))

# background screen color
color = (1,0,0)
ground_image = pygame.image.load('imgs/ground.png')

rat_image = pygame.image.load('imgs/fortnite.png')
cheeseImage = pygame.image.load('imgs/scar.png')
wallImage = pygame.image.load('imgs/grass4.png')
sucoglup_image = pygame.image.load('imgs/sucoglup.webp')

GROUND_IMAGE_SIZE = (cell_size, cell_size)
RAT_IMAGE_SIZE = (cell_size, cell_size)
CHEESE_IMAGE_SIZE = (cell_size, cell_size)
WALL_IMAGE_SIZE = (cell_size, cell_size)
SUCOGLUP_IMAGE_SIZE = (cell_size, cell_size)

# redimensionamento das imagens
ground_image = pygame.transform.scale(ground_image, GROUND_IMAGE_SIZE)
rat_image = pygame.transform.scale(rat_image, RAT_IMAGE_SIZE)
cheeseImage = pygame.transform.scale(cheeseImage, CHEESE_IMAGE_SIZE)
wallImage = pygame.transform.scale(wallImage, WALL_IMAGE_SIZE)
sucoglup_image = pygame.transform.scale(sucoglup_image, SUCOGLUP_IMAGE_SIZE)

# posições iniciais
positionRX = positionRX * cell_size
positionRY = positionRY * cell_size
positionCX = positionCX * cell_size
positionCY = positionCY * cell_size

pygame.time.wait(100)
pixels = cell_size

visited_cells = [[False] * w for _ in range(h)]

def mark_visited(maze, positionRX, positionRY):

    visited_cells[positionRY // cell_size][positionRX // cell_size] = True
    return visited_cells

def clear_previous_movement(maze, rat_positions):

    if len(rat_positions) > 1:
        prev_x, prev_y, _ = rat_positions[-2]
        maze[prev_y // cell_size][prev_x // cell_size] = 0

def get_valid_moves(positionRX, positionRY):
    moves = []
    for dx, dy in directions:
        new_x = positionRX + dx * cell_size
        new_y = positionRY + dy * cell_size
        new_x_index = new_x // cell_size
        new_y_index = new_y // cell_size

        if (
            0 <= new_x < width - RAT_IMAGE_SIZE[0]
            and 0 <= new_y < height - RAT_IMAGE_SIZE[1]
            and maze[new_y_index][new_x_index] in (0, 3)
            and not visited_cells[new_y_index][new_x_index]
        ):
            moves.append(((new_x, new_y), (dx, dy)))

    return moves

def tocar_som_vitoria():
    global som_reproduzido
    if not som_reproduzido:
        victory_royale.play()
        som_reproduzido = True


last_move_time = time.time()

rat_positions = deque()

correct_path = []

last_direction = (1, 0)

found_cheese = False  
message_display_time = None



running = True

while running:
    screen.fill(color)

    for i in range(h):
        for j in range(w):
            x = j * cell_size
            y = i * cell_size
            if maze[i][j] == 1:
                screen.blit(wallImage, (x, y))

    current_time = time.time()

    

    if current_time - last_move_time > 0.10 and not found_cheese:
        valid_moves = get_valid_moves(positionRX, positionRY)

        if valid_moves:
            next_move, next_direction = valid_moves[0]
            new_x, new_y = next_move

            correct_path.append((positionRX, positionRY))

            positionRX = new_x
            positionRY = new_y
            last_direction = next_direction

            rat_positions.append((positionRX, positionRY, last_direction))

            mark_visited(maze, positionRX, positionRY)
        else:
            if len(rat_positions) > 1:
                
                rat_positions.pop()

                last_x, last_y, last_direction = rat_positions[-1]

                positionRX = last_x
                positionRY = last_y

                correct_path.append((positionRX, positionRY))

            
            mark_visited(maze, positionRX, positionRY)

        last_move_time = current_time

    screen.blit(rat_image, (positionRX, positionRY))
    screen.blit(cheeseImage, (positionCX, positionCY))

    
    if (positionRX, positionRY) == (positionCX, positionCY) and not found_cheese:
        found_cheese = True
        message_display_time = pygame.time.get_ticks()

    if message_display_time is not None:
        current_ticks = pygame.time.get_ticks()
        if current_ticks - message_display_time < 10000:

            for x, y in correct_path:
                screen.blit(sucoglup_image, (x, y))
            
            file_path = 'right_way.txt'
            with open(file_path, 'w') as file:
                for x, y in correct_path:
                    file.write(f"{x},{y}\n")
        else:
            message_display_time = None
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
        
    if positionRX == positionCX and positionRY == positionCY:
        tocar_som_vitoria()
        posicao_imagem = ((width - largura_imagem) // 2, 1)
        screen.blit(imagem_fim_jogo, (posicao_imagem))
    
    pygame.display.update()
