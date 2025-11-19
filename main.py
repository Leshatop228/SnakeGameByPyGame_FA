import sys
import random
import pygame

pygame.init()

SIZE_BLOCK = 20
FRAME_COLOR = (128, 128, 128)
DARK_GRAY  = (51, 51, 51)
COUNT_BLOCKS = 20
GRAY = (100, 100, 100)
RED = (255, 66, 98)
MARGIN = 1
HEADER_MARGIN = 70
SNAKE_COLOR = (250, 250, 250)

size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN + COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN + COUNT_BLOCKS + HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Змейка")
timer = pygame.time.Clock()
courier = pygame.font.SysFont("arial", 25, bold=True, italic=False)

triangle_points = [(251, 35), (221, 50), (221, 20)]


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def get_random_empty_block(snake_blocks):
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
        empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
    return empty_block


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])
def start_or_restart_game(state):
    if state['GAME_OVER']:
        state['GAME_OVER'] = False
        state['IS_START'] = True
        state['snake_blocks'] = [SnakeBlock(9, 9), SnakeBlock(9, 10)]
        state['apple'] = get_random_empty_block(state['snake_blocks'])
        state['d_row'], state['d_column'] = 0, 1
        state['total'] = 0
        state['speed'] = 1
    else:

        state['IS_START'] = True


def handle_movement_keys(state, event):
    d_row, d_column = state['d_row'], state['d_column']
    if event.key == pygame.K_UP and d_column != 0:
        d_row, d_column = -1, 0
    elif event.key == pygame.K_DOWN and d_column != 0:
        d_row, d_column = 1, 0
    elif event.key == pygame.K_LEFT and d_row != 0:
        d_row, d_column = 0, -1
    elif event.key == pygame.K_RIGHT and d_row != 0:
        d_row, d_column = 0, 1
    return d_row, d_column


def handle_events(state, d_row, d_column):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not state['IS_START'] and point_in_triangle(event.pos, triangle_points):
                start_or_restart_game(state)
        if state['IS_START'] and event.type == pygame.KEYDOWN:
            d_row, d_column = handle_movement_keys(state, event)
            state['d_row'] = d_row  #
            state['d_column'] = d_column
    return state, state['d_row'], state['d_column']



def draw_header(total):
    pygame.draw.rect(screen, FRAME_COLOR, [0, 0, size[0], HEADER_MARGIN])
    text_total = courier.render(f"Хвост: {total}", 0, DARK_GRAY)
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))


def draw_game_field():
    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            draw_block(DARK_GRAY, row, column)


def draw_game(snake_blocks, apple):
    draw_game_field()
    draw_block(RED, apple.x, apple.y)
    for block in snake_blocks:
        draw_block(SNAKE_COLOR, block.x, block.y)


def point_in_triangle(point, tri):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    b1 = sign(point, tri[0], tri[1]) < 0.0
    b2 = sign(point, tri[1], tri[2]) < 0.0
    b3 = sign(point, tri[2], tri[0]) < 0.0
    return (b1 == b2) and (b2 == b3)


def button_play():
    mouse_pos = pygame.mouse.get_pos()
    if point_in_triangle(mouse_pos, triangle_points):
        color = GRAY
    else:
        color = DARK_GRAY
    pygame.draw.polygon(screen, color, triangle_points)


def update_snake(snake_blocks, d_row, d_column):
    head = snake_blocks[-1]
    new_head = SnakeBlock(head.x + d_row, head.y + d_column)
    snake_blocks.append(new_head)
    snake_blocks.pop(0)
    return snake_blocks

screen.fill(FRAME_COLOR)
draw_game_field()
pygame.display.flip()

state = {
    'IS_START': False,
    'GAME_OVER': False,
    'snake_blocks': [SnakeBlock(9, 9), SnakeBlock(9, 10)],
    'apple': get_random_empty_block([SnakeBlock(9, 9), SnakeBlock(9, 10)]),
    'd_row': 0,
    'd_column': 1,
    'total': 0,
    'speed': 1
}

while True:
    state, state['d_row'], state['d_column'] = handle_events(state, state['d_row'], state['d_column'])
    pygame.draw.rect(screen, FRAME_COLOR, [0, 0, size[0], HEADER_MARGIN])
    draw_header(state['total'])

    if not state['IS_START']:
        button_play()
    else:
        head = state['snake_blocks'][-1]

        if state['GAME_OVER']:
            draw_game(state['snake_blocks'], state['apple'])
            button_play()
        else:
            if not head.is_inside():
                state['IS_START'] = False
                state['GAME_OVER'] = True
            else:
                draw_game(state['snake_blocks'], state['apple'])
                if state['apple'] == head:
                    state['total'] += 1
                    state['speed'] = state['total'] // 5 + 1
                    state['snake_blocks'].append(state['apple'])
                    state['apple'] = get_random_empty_block(state['snake_blocks'])

                state['snake_blocks'] = update_snake(state['snake_blocks'], state['d_row'], state['d_column'])

    pygame.display.flip()
    timer.tick(4 + state['speed'])
