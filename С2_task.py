# Морской бой - задание по модулю С2


from random import randint
import time

class Dot: # координаты точки
    def __init__(self,x,y):
        self.x = x  #строка
        self.y = y #столбец

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __repr__(self): # для вывода в виде координат, а не в виде объекта
        return f'Dot({self.x},{self.y})'


class GameException(Exception):
    pass

class BoardOutException(GameException):
    def __str__(self):
        return "Выстрел вне поля!"

class UsedException(GameException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку. Попробуйте еще раз"

class WrongShipException(GameException):
    pass


class Ship:
    def __init__(self,cell_0,length,dir):
        self.cell_0 = cell_0
        self.length = length
        self.dir = dir
        self.lives = length

    @property
    def dots(self): #список всех точек корабля (метод repr выводит их как
        # координатыб а не как объекты)
        cell_x = self.cell_0.x
        cell_y = self.cell_0.y
        ship_dots = [Dot(cell_x,cell_y)] # начальная точка
        if self.length > 1:
            for i in range (2,self.length+1):
                if self.dir == 1:#расположение горизонтальное - слева направо
                    ship_dots.append (Dot(cell_x,cell_y+i-1))
                if self.dir == 0:# расположение вертикальное - сверху вниз
                    ship_dots.append(Dot(cell_x+i-1,cell_y))
        return ship_dots


    # def shooten(self,shot):
    #     return shot in self.dots


class Board: #игровая доска
    def __init__(self, hid=False, size=6):
        self.size = size #размерность доски
        self.hid = hid

        self.count = 0 # количество пораженных кораблей
        #поле  - двумерный список
        self.field = [['O' for j in range(size)] for i in range(size)]

        self.busy = [] #занятые точки
        self.ships = [] #список кораблей доски


    def __str__(self): #вывод поля на доску
        field_ = ''
        field_ += '\n   | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, j in enumerate(self.field):
            field_ += f"\n {i+1} | {' | '.join(j)} |"

        if self.hid:
            field_ = field_.replace("■", "O")

        return field_


    def out(self, d): #проверка на выход за пределы поля
            if ((0 <= d.x < self.size) and (0 <= d.y < self.size)):
                return False
            else:
                return True


    def add_ship(self, ship): # расстановка кораблей в поле

        for dot in ship.dots:
            if self.out(dot) or dot in self.busy: # проверка на возможность поставить корабль
                raise WrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False): #контур отображается только на доске противника
        near = [
            (-1, -1), (-1, 0), (-1, 1),(0, -1),
            (0, 1),(1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)


    def shot(self, dot):#выстрел по доске
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise UsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    if self.hid ==True:
                        self.contour(ship, verb=True)
                    else:
                        self.contour(ship, verb=False)
                    print("Корабль уничтожен!")
                    return True #игрок ходит снова
                else:
                    print("Корабль ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []




class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass
        # raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except GameException as e:
                print(e)

class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
        return dot

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = AI(comp, player)
        self.user = User(player, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self): #генерация случайной доски
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipException:
                    pass
        board.begin()
        return board


    def greet(self):

        print("                           Это игра Морской бой. ")
        print("      Правила игры: Расстановку кораблей производит компьютер случайным образом.")
        print("    У каждого игрока 1 трёхпалубный корабль, 2 двухпалубных и 3 обнопалубных корабля. ")
        print("                      В случае успешного попадания, игрок ходит повторно.   ")
        print("           -------------------------------------------------------------")
        print("            Для выстрела введите координаты клетки: x y через пробел ")
        print("                    x - номер строки,  y - номер столбца")
        print("                                     Удачи!")

    def loop(self):
        num = 0
        while True:
            time.sleep(1)
            print("        Ваше поле:")
            print(self.user.board)
            print("-" * 20)
            print("         Поле компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                # print("Ваш ход: ")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                time.sleep(3)
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Вы выиграли! УРА!")
                break

            if self.user.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()

