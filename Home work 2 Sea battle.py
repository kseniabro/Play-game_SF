from random import randint
from internal_logic import *
from time import sleep


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
        """
        Метод генерирует случайную доску.
        Закладываю 5 повторов (repeat) на добавление кораблей каждого типа.
        Если за 5 повторов не удается расположить корабли - начинаем снова формировать доску.
        """

        while True:
            board = Board(hid)
            direction = ["hor", "ver"]
            # Требуемое кол-во кораблей каждого типа.
            required_number_ships_type = [(3, 1), (2, 2), (1, 4)]  # (3,1) - 3хпалубный корабль в количетсве 1шт

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

    def __greet(self):
        print("""
        Добро пожаловать в игру "Морской бой". Игра представляет собой две доски 6х6.
        
        На доске размещается 7 кораблей: 
        - один на 3 клетки, 
        - два на 2 клетки 
        - и четыре на 1 клетку.
        
        Правила простые. 
        1) Корабли на досках размещаются автоматически, 
        пользователю нужно вводить только 
        координаты клетки, в которую он будет стрелять. 
        2) Коодинаты - целые числа от 1 до 6, вводятся через пробел.
        3) В стреляные клетки повторно стрелять нельзя.
        4) Побеждает тот игрок, который первым уничтожит флот противника.
        
        Обозначения:
        4) Х - Попадание.
        5) Т - промах.
        6) К - Корабль.
        
        Расширьте Ваше консольное окно, чтобы игровой процесс был более наглядным =)
        """)

    def __loop(self):
        """Метод с игровым циклом."""

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
        """Запуск игры."""

        self.__greet()
        self.__loop()
