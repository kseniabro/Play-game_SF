from random import randint
from internal_logic import *
from time import sleep

size_canvas_x = 600
size_canvas_y = 600
s_x = s_y = 6  # размер игрового поля
s_y = 6
step_x = size_canvas_x // s_x  # шаг по горизонтали
step_y = size_canvas_y // s_y  # шаг по вертикали
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
menu_x = 250
ships = s_x // 2  # определяем максимальное кол-во кораблей
ship_len1 = s_x // 3  # длина первого типа корабля
ship_len2 = s_x // 2  # длина второго типа корабля
ship_len3 = s_x // 1  # длина третьего типа корабля
enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
list_ids = []  # список объектов canvas

class Ship(object):
    def __init__(self, ship_type, cord, halo):
        self.ship_type = ship_type
        self.cord = cord
        self.halo = halo
        self.shoots = []
        self.state = u'Цел'

    def get_state(self):
        if len(self.shoots) == self.ship_type:
            self.state = u'Убил!'
        else:
            self.state = u'Попал!'
        return self.state

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
            print("Некорректный ввод. Координата - это два целых цисла от 1 до 6, разделенных пробелом!")
            return True
        except BoardOutException:
            print("Введенная координата находится за пределами доски!")
            return True
        except RetryException:
            print("По этой точке уже стреляли!")
            return True
        except ValueError:
            print("Некорректный ввод. Координата - это два целых цисла от 1 до 6, разделенных пробелом!")
            return True

        return False


class AI(Player):
    def _ask(self):
        # Выбор случайной точки.

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
            # Требуемое кол-во кораблей каждого типа.
            required_number_ships_type = [(3, 1), (2, 2), (1, 4)]  

            for type in required_number_ships_type:
                flag = False
                repeat = 0
                # Текущее кол-во кораблей каждого типа.
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

    
