import pygame
import sys
import numpy as np
from itertools import product

# Initialize pygame
pygame.init()

# Constants
SCREEN_SIZE = 600
GRID_SIZE = 3
DOT_RADIUS = 10
LINE_WIDTH = 5
MARGIN = 50
SPACE = (SCREEN_SIZE - 2 * MARGIN) // GRID_SIZE
DOT_COLOR = (0, 0, 0)
LINE_COLOR = (0, 0, 255)
PLAYER_COLOR = (0, 255, 0)
OPPONENT_COLOR = (255, 0, 0)
BG_COLOR = (255, 255, 255)
ANIMATION_SPEED = 5

# Screen setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Dots and Boxes")

# Board representation
# 0 = no line, 1 = player, 2 = opponent
horizontal_lines = np.zeros((GRID_SIZE, GRID_SIZE + 1), dtype=int)
vertical_lines = np.zeros((GRID_SIZE + 1, GRID_SIZE), dtype=int)
boxes = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Function to draw the grid
def draw_grid():
    screen.fill(BG_COLOR)
    for x, y in product(range(GRID_SIZE + 1), repeat=2):
        pygame.draw.circle(screen, DOT_COLOR, (MARGIN + x * SPACE, MARGIN + y * SPACE), DOT_RADIUS)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE + 1):
            if horizontal_lines[x, y] == 1:
                pygame.draw.line(screen, PLAYER_COLOR, (MARGIN + x * SPACE, MARGIN + y * SPACE),
                                 (MARGIN + (x + 1) * SPACE, MARGIN + y * SPACE), LINE_WIDTH)
            elif horizontal_lines[x, y] == 2:
                pygame.draw.line(screen, OPPONENT_COLOR, (MARGIN + x * SPACE, MARGIN + y * SPACE),
                                 (MARGIN + (x + 1) * SPACE, MARGIN + y * SPACE), LINE_WIDTH)

    for x in range(GRID_SIZE + 1):
        for y in range(GRID_SIZE):
            if vertical_lines[x, y] == 1:
                pygame.draw.line(screen, PLAYER_COLOR, (MARGIN + x * SPACE, MARGIN + y * SPACE),
                                 (MARGIN + x * SPACE, MARGIN + (y + 1) * SPACE), LINE_WIDTH)
            elif vertical_lines[x, y] == 2:
                pygame.draw.line(screen, OPPONENT_COLOR, (MARGIN + x * SPACE, MARGIN + y * SPACE),
                                 (MARGIN + x * SPACE, MARGIN + (y + 1) * SPACE), LINE_WIDTH)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if boxes[x, y] == 1:
                pygame.draw.rect(screen, PLAYER_COLOR, (MARGIN + x * SPACE + LINE_WIDTH // 2, MARGIN + y * SPACE + LINE_WIDTH // 2, SPACE - LINE_WIDTH, SPACE - LINE_WIDTH))
            elif boxes[x, y] == 2:
                pygame.draw.rect(screen, OPPONENT_COLOR, (MARGIN + x * SPACE + LINE_WIDTH // 2, MARGIN + y * SPACE + LINE_WIDTH // 2, SPACE - LINE_WIDTH, SPACE - LINE_WIDTH))

    pygame.display.update()

def animate_line(start_pos, end_pos, color):
    steps = 30
    for i in range(steps):
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * i // steps
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * i // steps
        pygame.draw.line(screen, color, start_pos, (x, y), LINE_WIDTH)
        pygame.display.update()
        pygame.time.delay(ANIMATION_SPEED)

def animate_box(x, y, color):
    rect = pygame.Rect(MARGIN + x * SPACE + LINE_WIDTH // 2, MARGIN + y * SPACE + LINE_WIDTH // 2, SPACE - LINE_WIDTH, SPACE - LINE_WIDTH)
    for i in range(0, SPACE - LINE_WIDTH, 5):
        pygame.draw.rect(screen, color, (rect.x, rect.y, i, rect.height))
        pygame.display.update()
        pygame.time.delay(ANIMATION_SPEED)

# Function to check and update the boxes
def check_boxes():
    global horizontal_lines, vertical_lines, boxes, current_player
    added = False
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if boxes[x, y] == 0 and horizontal_lines[x, y] and horizontal_lines[x, y + 1] and vertical_lines[x, y] and vertical_lines[x + 1, y]:
                boxes[x, y] = current_player
                animate_box(x, y, PLAYER_COLOR if current_player == 1 else OPPONENT_COLOR)
                added = True
    return added

# Function to check if game is over
def check_game_over():
    return np.all(horizontal_lines) and np.all(vertical_lines)

# Function to show end screen
def show_end_screen(player_score, opponent_score):
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont(None, 55)
    if player_score > opponent_score:
        text = font.render(f"You win! {player_score} : {opponent_score}", True, PLAYER_COLOR)
    elif opponent_score > player_score:
        text = font.render(f"You lose! {player_score} : {opponent_score}", True, OPPONENT_COLOR)
    else:
        text = font.render(f"Draw! {player_score} : {opponent_score}", True, DOT_COLOR)
    screen.blit(text, ((SCREEN_SIZE - text.get_width()) // 2, (SCREEN_SIZE - text.get_height()) // 2))
    pygame.display.update()
    pygame.time.wait(3000)

# Enhanced opponent strategy
def opponent_move():
    global horizontal_lines, vertical_lines, current_player, GRID_SIZE, boxes

    # Check for lines that complete boxes for the opponent
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE + 1):
            if horizontal_lines[x, y] == 0:
                horizontal_lines[x, y] = 2
                if check_boxes():
                    draw_grid()
                    pygame.time.delay(300)
                    continue
                horizontal_lines[x, y] = 0

    for x in range(GRID_SIZE + 1):
        for y in range(GRID_SIZE):
            if vertical_lines[x, y] == 0:
                vertical_lines[x, y] = 2
                if check_boxes():
                    draw_grid()
                    pygame.time.delay(300)
                    continue
                vertical_lines[x, y] = 0

    # Check for lines that open boxes for the player, if no immediate box to complete
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE + 1):
            if horizontal_lines[x, y] == 0:
                horizontal_lines[x, y] = 2
                if not check_boxes():
                    current_player = 1
                animate_line((MARGIN + x * SPACE, MARGIN + y * SPACE), (MARGIN + (x + 1) * SPACE, MARGIN + y * SPACE), OPPONENT_COLOR)
                return

    for x in range(GRID_SIZE + 1):
        for y in range(GRID_SIZE):
            if vertical_lines[x, y] == 0:
                vertical_lines[x, y] = 2
                if not check_boxes():
                    current_player = 1
                animate_line((MARGIN + x * SPACE, MARGIN + y * SPACE), (MARGIN + x * SPACE, MARGIN + (y + 1) * SPACE), OPPONENT_COLOR)
                return

    # Play a move that does not immediately open any boxes for the player
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE + 1):
            if horizontal_lines[x, y] == 0 and not opens_box(x, y, 2):
                horizontal_lines[x, y] = 2
                if can_complete_box(x, y, 2):
                    animate_line((MARGIN + x * SPACE, MARGIN + y * SPACE), (MARGIN + (x + 1) * SPACE, MARGIN + y * SPACE), OPPONENT_COLOR)
                    draw_grid()
                    return
                horizontal_lines[x, y] = 0

    for x in range(GRID_SIZE + 1):
        for y in range(GRID_SIZE):
            if vertical_lines[x, y] == 0 and not opens_box(x, y, 2):
                vertical_lines[x, y] = 2
                if can_complete_box(x, y, 2):
                    animate_line((MARGIN + x * SPACE, MARGIN + y * SPACE), (MARGIN + x * SPACE, MARGIN + (y + 1) * SPACE), OPPONENT_COLOR)
                    draw_grid()
                    return
                vertical_lines[x, y] = 0

    # If no move found that can close a box in immediate future, play any move that is available
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE + 1):
            if horizontal_lines[x, y] == 0:
                horizontal_lines[x, y] = 2
                animate_line((MARGIN + x * SPACE, MARGIN + y * SPACE), (MARGIN + (x + 1) * SPACE, MARGIN + y * SPACE), OPPONENT_COLOR)
                draw_grid()
                return

    for x in range(GRID_SIZE + 1):
        for y in range(GRID_SIZE):
            if vertical_lines[x, y] == 0:
                vertical_lines[x, y] = 2
                animate_line((MARGIN + x * SPACE, MARGIN + y * SPACE), (MARGIN + x * SPACE, MARGIN + (y + 1) * SPACE), OPPONENT_COLOR)
                draw_grid()
                return

# Function to check if a move opens a box for a given player
def opens_box(x, y, player):
    if y < GRID_SIZE and horizontal_lines[x, y] == 0 and horizontal_lines[x, y + 1] == 0 and vertical_lines[x, y] == 0 and vertical_lines[x + 1, y] == 0:
        return True
    if x < GRID_SIZE and vertical_lines[x, y] == 0 and vertical_lines[x + 1, y] == 0 and horizontal_lines[x, y] == 0 and horizontal_lines[x, y + 1] == 0:
        return True
    return False

# Function to check if a move can immediately close a box for a given player
def can_complete_box(x, y, player):
    if y < GRID_SIZE and horizontal_lines[x, y] == player and horizontal_lines[x, y + 1] == player and vertical_lines[x, y] == player and vertical_lines[x + 1, y] == player:
        return True
    if x < GRID_SIZE and vertical_lines[x, y] == player and vertical_lines[x + 1, y] == player and horizontal_lines[x, y] == player and horizontal_lines[x, y + 1] == player:
        return True
    return False

# Main game loop
current_player = 1
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            x, y = pos

            # Check horizontal lines
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE + 1):
                    x1 = MARGIN + i * SPACE
                    x2 = MARGIN + (i + 1) * SPACE
                    y1 = MARGIN + j * SPACE
                    if x1 <= x <= x2 and y1 - LINE_WIDTH // 2 <= y <= y1 + LINE_WIDTH // 2:
                        if horizontal_lines[i, j] == 0:
                            horizontal_lines[i, j] = current_player
                            animate_line((x1, y1), (x2, y1), PLAYER_COLOR if current_player == 1 else OPPONENT_COLOR)
                            if not check_boxes():
                                current_player = 3 - current_player
                            draw_grid()
                            break

            # Check vertical lines
            for i in range(GRID_SIZE + 1):
                for j in range(GRID_SIZE):
                    x1 = MARGIN + i * SPACE
                    y1 = MARGIN + j * SPACE
                    y2 = MARGIN + (j + 1) * SPACE
                    if y1 <= y <= y2 and x1 - LINE_WIDTH // 2 <= x <= x1 + LINE_WIDTH // 2:
                        if vertical_lines[i, j] == 0:
                            vertical_lines[i, j] = current_player
                            animate_line((x1, y1), (x1, y2), PLAYER_COLOR if current_player == 1 else OPPONENT_COLOR)
                            if not check_boxes():
                                current_player = 3 - current_player
                            draw_grid()
                            break

            if check_game_over():
                game_over = True
                player_score = np.sum(boxes == 1)
                opponent_score = np.sum(boxes == 2)
                show_end_screen(player_score, opponent_score)
                pygame.quit()
                sys.exit()

            if current_player == 2 and not game_over:
                opponent_move()
                draw_grid()
                if not check_boxes():
                    current_player = 1

                if check_game_over():
                    game_over = True
                    player_score = np.sum(boxes == 1)
                    opponent_score = np.sum(boxes == 2)
                    show_end_screen(player_score, opponent_score)
                    pygame.quit()
                    sys.exit()

    draw_grid()
