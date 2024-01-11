from random import randint
from time import sleep


# Размер игровой доски
BOARD_SIZE = 6
# Длины / количество палуб всех кораблей в порядке убывания
SHIPS_TYPES = [3, 2, 2, 1, 1, 1, 1]


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self) -> str:
        return '\n\tЭта точка за пределами игровой доски!\n'

class BoardUsedException(BoardException):
    def __str__(self) -> str:
        return '\n\tВы уже стреляли в эту точку!\n'

class BoardWrongShipException(BoardException):
    pass

class Dot():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: 'Dot') -> bool:
        return self.x == other.x and self.y == other.y

class Ship():
    def __init__(self, length: int, bow: Dot, direction: int) -> None:
        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length

    @property
    def dots(self) -> list[Dot]:
        dot_list = list()
        for i in range(self.length):
            x, y = self.bow.x, self.bow.y
            if self.direction == 0:
                x += i
            elif self.direction == 1:
                y += i
            dot_list.append(Dot(x, y))
        return dot_list

    def is_strike(self, dot: Dot) -> bool:
        return dot in self.dots

class Board():
    _is_hidden: bool = False
    
    def __init__(self) -> None:
        self.table = [['○'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ships = list()
        self.locked_dots = list()
        self.live_ships = len(SHIPS_TYPES)

    @property
    def is_hidden(self) -> bool:
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        if isinstance(value, bool):
            self._is_hidden = value
        else:
            raise ValueError('Параметр is_hidden должен быть True или False.')

    def add_ship(self, ship: Ship) -> None:
        for dot in ship.dots:
            if Board.out(dot) or dot in self.locked_dots:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.table[dot.x][dot.y] = '■'
            self.locked_dots.append(dot)
        self.ships.append(ship)
        self.mark_oreol(ship)

    def mark_oreol(self, ship: Ship, is_game: bool = False) -> None:
        neighbours = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                      (1, 0), (-1, 1), (0, 1), (1, 1)]
        for dot in ship.dots:
            for dx, dy in neighbours:
                x, y = dot.x + dx, dot.y + dy
                current_dot = Dot(x, y)
                if (not Board.out(current_dot)) and \
                   (current_dot not in self.locked_dots):
                    self.locked_dots.append(current_dot)
                    if is_game:
                        self.table[x][y] = '•'

    def show(self) -> None:
        print(' X| 1 2 3 4 5 6')
        print('Y◢ ____________')
        for row in range(BOARD_SIZE):
            print(row + 1, end=' | ')
            for col in range(BOARD_SIZE):
                cell = self.table[col][row]
                if self.is_hidden:
                    print('○', end=' ') if cell == '■' else print(cell, end=' ')
                else:
                    print(cell, end=' ')
            print('')
        print('\n')

    @staticmethod
    def out(dot: Dot) -> bool:
        return not (0 <= dot.x < BOARD_SIZE and 0 <= dot.y < BOARD_SIZE)

    def shot(self, dot: Dot) -> bool:
        if Board.out(dot):
            raise BoardOutException
        if dot in self.locked_dots:
            raise BoardUsedException
        self.locked_dots.append(dot)
        for ship in self.ships:
            if ship.is_strike(dot):
                ship.lives -= 1
                self.table[dot.x][dot.y] = '×'
                if ship.lives == 0:
                    self.live_ships -= 1
                    self.mark_oreol(ship, is_game=True)
                    print('\n\tКорабль потоплен!')
                    sleep(1)
                    return True
                else:
                    print('\n\tПопадание!')
                    sleep(1)
                    return True
        self.table[dot.x][dot.y] = '•'
        print('\n\tМимо.')
        sleep(1)
        return False

    def get_ready(self) -> None:
        self.locked_dots = list()

    def is_loser(self) -> bool:
        return self.live_ships == 0

class Player():
    def __init__(self, own_board: Board, opponent_board: Board) -> None:
        self.own_board = own_board
        self.opponent_board = opponent_board

    def ask(self):
        raise NotImplementedError(f'Определите ask в {self.__class__.__name__}.')

    def move(self) -> bool:
        while True:
            try:
                return self.opponent_board.shot(self.ask())
            except ValueError:
                print('\n\tВнимательнее, вводите две цифры через пробел.\n')
                sleep(1)
            except BoardException as e:
                print(e)
                sleep(1)

class AI(Player):
    def ask(self) -> Dot:
        x, y = randint(1, BOARD_SIZE), randint(1, BOARD_SIZE)
        print(f'x y = {x} {y}')
        sleep(1)
        return Dot(x - 1, y - 1)

class User(Player):
    def ask(self) -> Dot:
        x, y = input('x y = ').strip().split()
        if x and y:
            return Dot(int(x) - 1, int(y) - 1)
        else:
            raise ValueError


class Game():
    def __init__(self) -> None:
        self.user_board = self.make_board()
        self.ai_board = self.make_board()
        self.ai_board.is_hidden = True
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def make_board(self) -> Board:
        board = None
        while board is None:
            board = Game.random_board()
        board.get_ready()
        return board

    @staticmethod
    def random_board() -> Board:
        board = Board()
        attempts = 0
        for length in SHIPS_TYPES:
            while True:
                if attempts > 2000:
                    return None
                try:
                    board.add_ship(Ship(length,
                                        Dot(randint(0, BOARD_SIZE-1),
                                            randint(0, BOARD_SIZE-1)
                                            ),
                                        randint(0, 1)
                                        )
                                   )
                    break
                except BoardWrongShipException:
                    pass
                attempts += 1
        return board

    @staticmethod
    def greet() -> None:
        text = """
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
        """
        
        marks = """
        Обозначения:
            ■ - палуба
            • - мимо / ореол корабля
            ○ - море
            × - попадание
        """
        print(text)
        print(marks)
        input('\n\tНажмите -= Enter =- для старта')

    def show_boards(self) -> None:
        print('\n\n\n' + '-' * 50)
        print('Доска пользователя:\n')
        self.user.own_board.show()
        print('Доска компьютера:\n')
        self.ai.own_board.show()

    def loop(self) -> None:
        player = 0
        while True:
            self.show_boards()
            if player % 2 == 0:
                print('Ваш ход:')
                repeat = self.user.move()
            else:
                print('Ходит компьютер:')
                repeat = self.ai.move()
            player += 0 if repeat else 1
            if self.ai.own_board.is_loser():
                print('\n\n\n' + '-' * 50 + '\n\n\n')
                print('#' * 22 + '\n#    Вы выиграли!    #\n' + '#' * 22)
                self.show_boards()
                break
            if self.user.own_board.is_loser():
                print('\n\n\n' + '-' * 50 + '\n\n\n')
                print('#' * 22 + '\n# Компьютер выиграл! #\n' + '#' * 22)
                self.show_boards()
                break

    def start(self) -> None:
        Game.greet()
        self.loop()


if __name__ == '__main__':
    game = Game()
    game.start()
    
