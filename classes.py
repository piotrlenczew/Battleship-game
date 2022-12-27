from random import randint


class WrongAmountOfRowsError(Exception):
    pass


class WrongAmountOfSquaresInRowsError(Exception):
    pass


class WrongIndicationOfSquare(Exception):
    pass


class MoreThanOneSymbolInSquareError(Exception):
    pass


class PositionOutOfBoardError(IndexError):
    pass


class IncorrectDirectionError(Exception):
    pass


class IncorrectLengthOfShipError(Exception):
    pass


class CanNotPlaceShipError(Exception):
    pass


class IncorrectSizeError(Exception):
    pass


class IncorrectPositioningOfShip(Exception):
    pass


class IncorrectPositionError(Exception):
    pass


# s - South, e - East
class Ship:
    """
    Class Ship. Contains attributes:
    :parametr position: tuple made up of two intigers indicating row and column
    :type position: tuple

    :param direction: can only be s - South or e - East
    :type direction: str

    :param length: number of squares that form ship
    :type length: int
    """
    def __init__(self, position, direction, length):
        try:
            if len(position) != 2:
                raise IncorrectPositionError('More than 2 dimensions given')
        except TypeError:
            raise IncorrectPositionError('Only one dimension given')
        self._position = position
        if direction != 's' and direction != 'e':
            message = 'Directions can only be: s - South or e - East'
            raise IncorrectDirectionError(message)
        self._direction = direction
        if length < 1:
            raise IncorrectLengthOfShipError('Ship must have positive length')
        self._length = length

    def position(self):
        return self._position

    def direction(self):
        return self._direction

    def length(self):
        return self._length

    def fits_in_board(self, size):
        """
        Checks if the ship fits in board of certain size
        """
        if size <= 0:
            raise IncorrectSizeError('Size needs to be positive')
        row, column = self._position
        if self._direction == 's':
            if row + self._length > size:
                return False
        else:
            if column + self._length > size:
                return False
        return True

    def positions(self):
        """
        Returns a list of square positions that form the ship
        """
        row, column = self._position
        result = []
        if self._direction == 's':
            for addend in range(self._length):
                result.append((row + addend, column))
        else:
            for addend in range(self._length):
                result.append((row, column + addend))
        return result


def correct_symbol_square(square):
    if square != ' ' and square != '~':
        if square != 'O' and square != 'X':
            return False
    return True


class BattleshipBoard:
    """
    Class BattleshipBoard. Contains attributes:
    :parametr size: indicates number of rows and columns
    :type size: int

    :param board: it is a list containing rows which are lists of squares,
    that can be ' ' - sea, '~' - attacked sea, 'O' - ship, 'X' - attacked ship
    :type board: list
    """
    def __init__(self, size, board=None):
        if size <= 0:
            raise IncorrectSizeError('Size needs to be positive')
        self._size = size
        if not board:
            board = [[' '] * size for row in range(size)]
        else:
            if len(board) != size:
                message = f'Amount of rows needs to be {size}'
                raise WrongAmountOfRowsError(message)
            for row in board:
                if len(row) != size:
                    message = f"At least one row doesn't have {size} elements"
                    raise WrongAmountOfSquaresInRowsError(message)
                for square in row:
                    if len(square) != 1:
                        message = 'Square can only be a single symbol'
                        raise MoreThanOneSymbolInSquareError(message)
                    elif not correct_symbol_square(square):
                        message = 'Forbidden symbol in one of the squares'
                        raise WrongIndicationOfSquare(message)
        self._board = board

    def board(self):
        return self._board

    def size(self):
        return self._size

    # def set_board(self, new_size, new_board):
    #     if len(new_board) != new_size:
    #         message = f'Amount of rows needs to be {new_size}'
    #         raise WrongAmountOfRowsError(message)
    #     for row in new_board:
    #         if len(row) != new_size:
    #             message = f"At least one row doesn't have {new_size} elements"
    #             raise WrongAmountOfSquaresInRowsError(message)
    #         for square in row:
    #             if len(square) != 1:
    #                 message = 'Square can only be a single symbol'
    #                 raise MoreThanOneSymbolInSquareError(message)
    #             elif not correct_symbol_square(square):
    #                 message = 'Forbidden symbol in one of the squares'
    #                 raise WrongIndicationOfSquare(message)
    #     self._board = new_board
    #     self._size = new_size

    def get_square(self, position):
        """
        Returns square in given position
        """
        row, column = position
        try:
            return self._board[row][column]
        except IndexError:
            size = self._size
            message = f'There is no such position in {size}x{size} board'
            raise PositionOutOfBoardError(message)

    def set_square(self, position, indication):
        """
        Allows to change square in given position to given indication
        """
        if len(indication) != 1:
            message = 'Square can only be a single symbol'
            raise MoreThanOneSymbolInSquareError(message)
        if not correct_symbol_square(indication):
            message = 'Forbidden symbol given'
            raise WrongIndicationOfSquare(message)
        row, column = position
        try:
            self._board[row][column] = indication
        except IndexError:
            size = self._size
            message = f'There is no such position in {size}x{size} board'
            raise PositionOutOfBoardError(message)

    def has_ship(self):
        """
        Checks if there is any ship in board
        """
        for row in self._board:
            for square in row:
                if square == 'O':
                    return True
        return False

    def ship_near(self, position):
        """
        Checks if there is a ship around given point including diagonally
        """
        row, column = position
        if row > 9 or column > 9 or row < 0 or column < 0:
            size = self._size
            message = f'There is no such position in {size}x{size} board'
            raise PositionOutOfBoardError(message)
        for row_difference in range(-1, 2):
            for column_difference in range(-1, 2):
                try:
                    current_row = row + row_difference
                    current_column = column + column_difference
                    current_square = self._board[current_row][current_column]
                    if current_square == 'X' or current_square == 'O':
                        return True
                except IndexError:
                    pass
        return False

    def can_place_ship(self, ship):
        """
        checks if there is possibility to place given ship in board
        """
        if not ship.fits_in_board(self._size):
            return False
        ship_positions = ship.positions()
        for position in ship_positions:
            if self.ship_near(position):
                return False
        return True

    def place_ship(self, ship):
        """
        Places ship in board
        """
        if self.can_place_ship(ship):
            ship_positions = ship.positions()
            for position in ship_positions:
                self.set_square(position, 'O')
        else:
            message = "Ship doesn't fit in board or interferes with other ship"
            raise CanNotPlaceShipError(message)

    def __str__(self):
        result = ' '
        for number in range(self._size):
            result = result + ' ' + str(number)
        result = result + '\n'
        for index, row in enumerate(self._board):
            result = result + str(index)
            for square in row:
                result = result + ' ' + square
            result = result + '\n'
        return result


class Player():
    def __init__(self):
        self._player_board = BattleshipBoard()
        self._player_guess_board = BattleshipBoard()

    def guess(self, computer_board, position):
        square = computer_board.get_square(position)
        if square == 'O':
            computer_board.set_square(position, 'X')
            self._player_guess_board.set_square(position, 'X')
        elif square == ' ':
            computer_board.set_square(position, '~')
            self._player_guess_board.set_square(position, '~')
        else:
            pass

    def place_ship(self, ship):
        self._player_board.place_ship(ship)


def generate_ship(length):
    row = randint(0, 9)
    column = randint(0, 9)
    condition = randint(0, 1)
    if condition == 0:
        direction = 's'
    else:
        direction = 'e'
    ship = Ship((row, column), direction, length)
    return ship


class ComputerPlayer():
    def __init__(self):
        self._computer_board = BattleshipBoard()
        self._last_guess = None

    def guess(self, player_board, position=None):
        if not position:
            pass
        else:
            square = player_board.get_square(position)
            if square == 'O':
                player_board.set_square(position, 'X')
                self._computer_board

    def place_ships(self, list_of_ships=None):
        pass
