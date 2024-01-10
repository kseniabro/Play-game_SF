from random import randint

board_ai = Game.random_board()
board_user = Game.random_board(hid=False)

user = User(board_user, board_ai)
ai = AI(board_ai, board_user)

game = Game(user, ai)
game.start()

class Dot:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __setattr__(self, key, value):
        if (key == "_Dot__x" or key == "_Dot__y") and type(value) != int:
            raise AttributeError
        else:
            super().__setattr__(key, value)


class Ship:
    def __init__(self, len_ship: int, dot_bow: Dot, direction: str):
        self.__len_ship = len_ship
        self.__dot_bow = dot_bow
        self.__direction = direction
        self.__volume = len_ship
    def dots(self):
        if self.__direction == "ver":
            return [Dot(self.__dot_bow.x + i, self.__dot_bow.y) for i in range(0, self.__len_ship)]
        elif self.__direction == "hor":
            return [Dot(self.__dot_bow.x, self.__dot_bow.y + j) for j in range(0, self.__len_ship)]
        else:
            pass

    @property
    def len_ship(self):
        return self.__len_ship

    @property
    def dot_bow(self):
        return self.__dot_bow

    @property
    def direction(self):
        return self.__direction

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, new_volume):
        self.__volume = new_volume

    def __setattr__(self, key, value):
        if key == "_Ship__len_ship" and (not (1 <= value <= 3) or type(value) != int):
            raise AttributeError
        elif key == "_Ship__direction" and value not in ["hor", "ver"]:
            raise AttributeError
        else:
            super().__setattr__(key, value)


class Board:
    def __init__(self, hid=True):
        self.__board_list = [["o" for i in range(6)] for j in range(6)]
        self.__list_ship = []
        self.__hid = hid
        self.__number_living_ships = 0

    @property
    def number_living_ships(self):
        return self.__number_living_ships

    @property
    def list_ship(self):
        return self.__list_ship

    def __chek_position_ship(self, ship: Ship):
        for dot in ship.dots():
            if self.__out(dot):
                raise BoardOutException
        for ship_on_board in self.__list_ship:
            for dot in ship.dots():
                if dot in self.__contour(ship_on_board):
                    raise ShipPositionException
        return True

    def add_ship(self, ship: Ship):
        if self.__chek_position_ship(ship):
            self.__list_ship.append(ship)
            self.__number_living_ships += 1
            for dot in ship.dots():
                self.__board_list[dot.x-1][dot.y-1] = "K"

    def __contour(self, ship: Ship):
        dot_in_comtour = []
        dot_in_comtour.extend(ship.dots())

        x = ship.dot_bow.x
        y = ship.dot_bow.y
        len_ship = ship.len_ship

        if ship.direction == "ver":
            dot_in_comtour.extend([Dot(x+i, y-1) for i in range(0, len_ship)])
            dot_in_comtour.extend([Dot(x+i, y+1) for i in range(0, len_ship)])
            dot_in_comtour.extend([Dot(x-1, y), Dot(x-1, y-1), Dot(x-1, y+1)])
            dot_in_comtour.extend([Dot(x+len_ship, y), Dot(x+len_ship, y-1), Dot(x+len_ship, y+1)])
        elif ship.direction == "hor":
            dot_in_comtour.extend([Dot(x+1, y+i) for i in range(0, len_ship)])
            dot_in_comtour.extend([Dot(x-1, y+i) for i in range(0, len_ship)])
            dot_in_comtour.extend([Dot(x, y-1), Dot(x-1, y-1), Dot(x+1, y-1)])
            dot_in_comtour.extend([Dot(x, y+len_ship), Dot(x+1, y+len_ship), Dot(x-1, y+len_ship)])

        return dot_in_comtour

    def print_board(self):
        string = '{:^2}' * 7
        print(string.format('', *range(1, 7)))

        for num_row, cell in enumerate(self.__board_list):
            if not self.__hid:
                print(string.format(num_row + 1, *cell))
            else:
                cell = "".join(cell).replace("K", "o")
                print(string.format(num_row + 1, *cell))

    def __out(self, dot: Dot):
        if 1<=dot.x<=6 and 1<=dot.y<=6:
            return False
        return True

    def shot(self, dot: Dot):
        if self.__out(dot):
            raise BoardOutException

        if self.__board_list[dot.x-1][dot.y-1] in ["X", "T"]:
            raise RetryException

        flag = False

        for ship in self.__list_ship:
            for dot_ship in ship.dots():
                if dot == dot_ship:
                    flag = True
                    ship.volume -= 1
                    if ship.volume == 0:
                        self.__number_living_ships -= 1
                    break
        if flag:
            self.__board_list[dot.x-1][dot.y-1] = "X"
            print("Попадание!")
            return True
        else:
            self.__board_list[dot.x-1][dot.y-1] = "T"
            print("Мимо")

class Player:
    def __init__(self, board: Board, board_other: Board):
        self.__board = board
        self.__board_other = board_other

    @property
    def board(self):
        return self.__board

    def _ask(self):
        pass

    def move(self):
        try:
            koords = self._ask()
            if self.__board_other.shot(Dot(koords[0], koords[1])):
                return True
        except AttributeError:
            print("Некорректный ввод")
            return True
        except BoardOutException:
            print("Выстрел за пределами доски")
            return True
        except RetryException:
            print("По этой точке уже стреляли")
            return True
        except ValueError:
            print("Некорректный ввод")
            return True

        return False


class AI(Player):
    def _ask(self):
        return randint(1, 6), randint(1, 6)


class User(Player):
    def _ask(self):
        x, y = list(map(int, input("Введите координаты точки x и y через пробел: ").split()))
        return x, y


class Game:
    def __init__(self, user: User, ai: AI):
        self.__user = user
        self.__board_user = user.board
        self.__ai = ai
        self.__board_ai = ai.board

    @staticmethod
    def random_board(hid=True):
        while True:
            board = Board(hid)
            direction = ["hor", "ver"]
            required_number_ships_type = [(3, 1), (2, 2), (1, 4)] 
            for type in required_number_ships_type:
                flag = False
                repeat = 0
                current_number_ships = 0

                while current_number_ships != type[1]:
                    try:
                        board.add_ship(Ship(type[0], Dot(randint(1, 6), randint(1, 6)), direction[randint(0, 1)]))
                        current_number_ships = len(list(filter(lambda x: x.len_ship == type[0], board.list_ship)))
                    except (BoardOutException, ShipPositionException):
                        repeat += 1
                        if repeat == 5 and len(board.list_ship) != 7:
                            flag = True
                            break
                if flag:
                    break
            if len(board.list_ship) == 7:
                break

        return board

class BoardOutException(Exception):
    pass

class ShipPositionException(Exception):
    pass

class RetryException(Exception):
    passclass BoardOutException(Exception):
    pass

class ShipPositionException(Exception):
    pass

class RetryException(Exception):
    pass


    def __greet(self):
        print("""
        Добро пожаловать в игру "Морской бой". Игра представляет собой поле 6х6.
        
        На поле размещается 7 кораблей: 
        - один на 3 клетки, 
        - два на 2 клетки 
        - и четыре на 1 клетку.
        
        1) Корабли на досках размещаются автоматически, 
        пользователю нужно вводить только 
        координаты клетки, в которую он будет стрелять. 
        2) Коодинаты - целые числа от 1 до 6, вводятся через пробел.
        3) В клетки повторно стрелять нельзя.
        4) Побеждает тот игрок, который первым уничтожит флот противника.
        
        Обозначения:
        4) Х - Попадание.
        5) Т - промах.
        6) К - Корабль.
    
        """)

    def __loop(self):
        def loop(board: Board, player: Player, board_other: Board,
                 player_name: str, field: str, delimiter: str):

            while True:
                sleep(2)
                print(f"Ход {player_name}.", f"Поле {field}:", delimiter * 15, sep="\n")
                board.print_board()
                if player.move():
                    board.print_board()
                    print(delimiter * 15)
                    if board_other.number_living_ships == 0:
                        print(f"Игра окончера, победил {player_name}!")

                        return True
                    continue
                else:
                    board.print_board()
                    print(delimiter * 15)
                    break
            sleep(2)

        while True:
            if loop(self.__ai.board, self.__user,
                    self.__board_ai, "USER", "AI", "*"):
                break
            if loop(self.__user.board, self.__ai,
                    self.__board_user, "AI", "USER", "-"):
                break

    def start(self):

        self.__greet()
        self.__loop()



