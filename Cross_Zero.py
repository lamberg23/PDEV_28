# Игра "Крестики - нолики "

def info():
    print('       Это игра "Крестики-Нолики"')
    print('       "X" и "O" ходят по очереди. Начинает всегда "X".')
    print('       Для хода в игре необходимо вводить координаты клетки.')
    print('       Вначале всегда указывается номер строки, а затем номер столбца')

def play_field ():  # вывод игрового поля
    print()
    print ('                         0  1  2')
    for i,j in enumerate (cell):
        row_field = f"                      {i}  {'  '.join(j)} "
        print(row_field)



def move_correct(): # проверка правильности ввода: 1) существуют ли координаты; 2) не заполнена ли клетка
    while True:
        act = input(f'    Введите номер строки и столбца через пробел: ').split()
        if len (act)!= 2:
            print('Вы ввели некорректные координаты. Введите номер строки и столбца через пробел')
            x,y = act
        else:
            x, y = map(int, act)
        if x < 0 or x > 2 or y < 0 or y > 2:
            print('Вы ввели некорректные координаты. Введите номер строки и столбца через пробел')
            x,y = act

        if cell[x][y]!= '_':
            print('Клетка занята. Введите другие координаты:')
            x,y =act
        else:
            return x,y



def winner(): # выигрышные комбинации

    if cell[0][0] == cell[0][1] == cell[0][2] != '_': #  первая линия
        return True
    elif cell[1][0] == cell[1][1] == cell[1][2] != '_': # вторая линия
        return True
    elif cell[2][0] == cell[2][1] == cell[2][2] != '_': # третья линия
        return True
    elif cell[0][0] == cell[1][0] == cell[2][0] != '_': # первая вертикаль
        return True
    elif cell[0][1] == cell[1][1] == cell[2][1] != '_':  # вторая вертикаль
        return True
    elif cell[0][2] == cell[1][2] == cell[2][2] != '_':  # третья вертикаль
        return True
    elif cell[0][0] == cell[1][1] == cell[2][2] != '_':  # первая диагональ
        return True
    elif cell[2][0] == cell[1][1] == cell[0][2] != '_':  # вторая диагональ
        return True
    else:
        return False


info()
cell = [['_' for j in range(3)] for i in range(3)]
step = 0 # счетчик ходов
while True:
    play_field()
    step += 1
    if step % 2 == 0:
        player = 'O'
    else:
        player = 'X'
    print(f'     Ход {player}')

    x,y = move_correct()
    cell[x][y] = player

    if winner():
        print(f' {player} выиграл!')
        play_field()
        break
    elif step == 9:
        print(f'Ничья!')
        break