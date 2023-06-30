import pygame
from random import randint
from copy import deepcopy

print("\n\n\n\n\n---------------------------------Привет!-------------------------------\n Это симулятор жизни клеток под названием \'Conway's game of life\' в котором появляются или исчезают клетки по данным правилам:")
print('• Текущая клетка умирает если у нее есть более 3 или менее 2 соседей \n• Текущая клетка появляется если у этой клетки есть 3 соседа')
print('\n для начала игры необходимо ввести начальные условия(цифру):')
print('• Рандомная генерация(1)               • Горизонтальная и вертикальная линии пересекающиеся в центре(2)')
print('• Вертикальные линии(3)                • Шахматы с пустой линией(4)(при размере клетки == 10)')
print('• Миллиметровка(5)                     • Диагональные линии(6)(при размере клетки == 10)')
conditional = int(input('Начальные условия № '))

if conditional > 6 or conditional < 1:
    print('\n\n                 Начальное условие выбрано неправильно => выход')
    exit()

RES = WIDTH, HEIGHT = 1400, 800
TILE = int(input('Введите размер одной клетки(усл.ед >= 3) '))
W, H = WIDTH // TILE, HEIGHT // TILE

if TILE < 3:
    print('\n\n                 Размер клетки выбран неправильно => выход')
    exit()

FPS = int(input('Введите скорость изменений(FPS): '))

if FPS < 1:
    print('\n\n                 FPS выбрано неправильно => выход')
    exit()

yellow = (255,255,122)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
gray = (120, 120, 120)
green = (0, 255, 0)
violet = (75, 0, 130)
border = (30, 30, 30)

conditional_color = int(input(('Выберите цвет клеток(напишите цифру): желтый(1), синий(2), белый(3), серый(4), зеленый(5), фиолетовый(6) - ')))

cell_color = (0, 0, 0)

if conditional_color == 1:
    cell_color = yellow
elif conditional_color == 2:
    cell_color = blue
elif conditional_color == 3:
    cell_color = white
elif conditional_color == 4:
    cell_color = gray
elif conditional_color == 5:
    cell_color = green
elif conditional_color == 6:
    cell_color = violet
else:
    print('\n\n                 Цвет выбран неправильно => выход')
    exit()


pygame.init()
display = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption('Conway\'s game of life')

# message on display
font_style = pygame.font.SysFont('bahnschrift', 30)
def message_dis(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [0, 0])

next_field = [[0 for i in range(W)] for j in range(H)]

if conditional == 1:
    current_field = [[randint(0, 1) for i in range(W)] for j in range(H)]
elif conditional == 2:
    current_field = [[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)]
elif conditional == 3:
    current_field = [[1 if not i % 10 else 0 for i in range(W)] for j in range(H)]
elif conditional == 4:
    current_field = [[1 if not (2 * i + j) % 4 else 0 for i in range(W)] for j in range(H)]
elif conditional == 5:
    current_field = [[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)]
elif conditional == 6:
    current_field = [[1 if i == j + W / 4 or W - i == j + W/4 else 0 for i in range(W)] for j in range(H)]

def check_cell(current_field, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0

FPS_counter = 0
while True:

    display.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # draw grid
    [pygame.draw.line(display, border, (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pygame.draw.line(display, border, (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]

    # draw life
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            if current_field[y][x]:
                pygame.draw.rect(display, cell_color, (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
            next_field[y][x] = check_cell(current_field, x, y)
    current_field = deepcopy(next_field)
    if conditional == 1:
        message_dis("Рандомная генерация", red)
    elif conditional == 2:
        message_dis("Гор. и верт. линии", red)
    elif conditional == 3:
        message_dis("Верт. линии", red)
    elif conditional == 4:
        message_dis("Псевдно-шахматы", red)
    elif conditional == 5:
        message_dis("Миллиметровка", red)
    elif conditional == 6:
        message_dis("Диаг. линии", red)

    clock.tick(FPS)
    pygame.display.flip()
    if FPS_counter == 10:
        FPS_counter = 0
        print('Текущий FPS == ' + str(clock.get_fps()))
    else:
        FPS_counter = FPS_counter + 1