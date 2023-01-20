from game_files.defined_enumerations import Direction
from game_files.game_settings import (
    sea_ind, attacked_sea_ind, ship_ind, attacked_ship_ind
)
from game_files.ship import Ship


class WrongAmountOfRowsError(Exception):
    """Not enough or too much rows."""
    pass


class WrongAmountOfSquaresInRowsError(Exception):
    """Not enough or too much squares in row."""
    pass


class WrongIndicationOfSquare(Exception):
    """Inappropriate square indication."""
    pass


class MoreThanOneSymbolInSquareError(Exception):
    """Square indication of more than one symbol."""
    pass


class PositionOutOfBoardError(IndexError):
    """Position out of board."""
    pass


class CanNotPlaceShipError(Exception):
    """Ship can't be placed in board."""
    pass


class IncorrectSizeError(Exception):
    """Inappropriate size of board."""
    pass


class IncorrectPositioningOfShip(Exception):
    """Ship impossible to be in board."""
    pass


def correct_symbol_square(square):
    """Return True if correct indication of square else False"""
    if square != sea_ind and square != attacked_sea_ind:
        if square != ship_ind and square != attacked_ship_ind:
            return False
    return True


class BattleshipBoard:
    """
    Class BattleshipBoard. Contains attributes:
    :parametr size: indicates number of rows and columns
    :type size: int

    :param board: it is a list containing rows which are lists of squares,
    with indications defined in square_indications.py file
    :type board: list
    """
    def __init__(self, size, board=None):
        """Initializeinstance of BattleshipBoard."""
        if size <= 0:
            raise IncorrectSizeError('Size needs to be positive')
        self._size = size
        if not board:
            board = [[sea_ind] * size for row in range(size)]
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
        """Get board attribute."""
        return self._board

    def size(self):
        """Get size attribute."""
        return self._size

    def get_square(self, position):
        """Return square in given position."""
        row, column = position
        try:
            return self._board[row][column]
        except IndexError:
            size = self._size
            message = f'There is no such position in {size}x{size} board'
            raise PositionOutOfBoardError(message)

    def set_square(self, position, indication):
        """Change square in given position to given indication."""
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

    def position_in_board(self, position):
        """Check if position is in board."""
        row, column = position
        size = self._size
        if row < 0 or row > size - 1 or column < 0 or column > size - 1:
            return False
        return True

    def has_ship(self):
        """Check if there is any ship in board."""
        for row in self._board:
            for square in row:
                if square == ship_ind:
                    return True
        return False

    def ship_near(self, position):
        """Check if there is a ship around given point including diagonally."""
        row, column = position
        size = self._size
        if row > size - 1 or column > size - 1 or row < 0 or column < 0:
            message = f'There is no such position in {size}x{size} board'
            raise PositionOutOfBoardError(message)
        for row_difference in range(-1, 2):
            for column_difference in range(-1, 2):
                try:
                    current_row = row + row_difference
                    current_column = column + column_difference
                    current_square = self._board[current_row][current_column]
                    if current_row >= 0 and current_column >= 0:
                        if current_square == attacked_ship_ind or current_square == ship_ind:
                            return True
                except IndexError:
                    pass
        return False

    def can_place_ship(self, ship):
        """Check if there is possibility to place given ship in board."""
        if not ship.fits_in_board(self._size):
            return False
        ship_positions = ship.positions()
        try:
            for position in ship_positions:
                if self.ship_near(position):
                    return False
            return True
        except PositionOutOfBoardError:
            return False

    def place_ship(self, ship):
        """Place ship in board."""
        if self.can_place_ship(ship):
            ship_positions = ship.positions()
            for position in ship_positions:
                self.set_square(position, ship_ind)
        else:
            message = "Ship doesn't fit in board or interferes with other ship"
            raise CanNotPlaceShipError(message)

    def set_if_in_board(self, position, indication):
        """Set square in given position to given indication if in board."""
        row, column = position
        if row >= 0 and column >= 0 and row < self.size() and column < self.size():
            self.set_square(position, indication)

    def set_squares_around_ship(self, ship, indication):
        """Set squares around given ship to given indication."""
        position = ship.position()
        row, column = position
        direction = ship.direction()
        length = ship.length()
        if direction == Direction.vertical:
            addends = [
                (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1),
                (length - 1, 1), (length, 1), (length, 0),
                (length, -1), (length - 1, -1)
            ]
            for row_addend, column_addend in addends:
                self.set_if_in_board((row + row_addend, column + column_addend), indication)
            for number in range(1, length - 1):
                self.set_if_in_board((row + number, column + 1), indication)
                self.set_if_in_board((row + number, column - 1), indication)
        else:
            addends = [
                (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0),
                (1, length - 1), (1, length), (0, length),
                (-1, length), (-1, length - 1)
            ]
            for row_addend, column_addend in addends:
                self.set_if_in_board((row + row_addend, column + column_addend), indication)
            for number in range(1, length - 1):
                self.set_if_in_board((row + 1, column + number), indication)
                self.set_if_in_board((row - 1, column + number), indication)

    def remove_ship(self, ship):
        """Change squares where given ship would be to sea_ind."""
        ship_positions = ship.positions()
        for position in ship_positions:
            try:
                self.set_square(position, sea_ind)
            except PositionOutOfBoardError:
                raise IncorrectPositioningOfShip("Such ship can't be in board")

    def get_if_in_board(self, position):
        """Return square indication if square in board, else None."""
        row, column = position
        try:
            return self.get_square((row, column))
        except PositionOutOfBoardError:
            return None

    def find_nearest_att_ship(self, position):
        """
        Should be used when square in given position is attacked_sea
        Return position of adjacent attacked_ship
        If there isn't any return None
        """
        row, column = position
        s_square = self.get_if_in_board((row + 1, column))
        if s_square:
            if s_square == attacked_ship_ind:
                return (row + 1, column)
        n_square = self.get_if_in_board((row - 1, column))
        if n_square:
            if n_square == attacked_ship_ind:
                return (row - 1, column)
        e_square = self.get_if_in_board((row, column + 1))
        if e_square:
            if e_square == attacked_ship_ind:
                return (row, column + 1)
        w_square = self.get_if_in_board((row, column - 1))
        if w_square:
            if w_square == attacked_ship_ind:
                return (row, column - 1)
        return None

    def one_way_ship_length_is_sunk(self, position, addends):
        """
        Counts attacked ship squares until it finds other indication in one way.

        if it is attacked sea returns length and True for sunk ship
        if it is sea returns length and False for not sunk ship
        if ship it returns None to indicate that it can't be sunk ship
        """
        row, column = position
        add_row, add_column = addends
        length = 0
        while True:
            try:
                row += add_row
                column += add_column
                if row >= 0 and column >= 0 and row < self._size and column < self._size:
                    current_square = self.get_square((row, column))
                    if current_square == attacked_ship_ind:
                        length += 1
                    elif current_square == attacked_sea_ind:
                        return (length, True)
                    elif current_square == sea_ind:
                        return (length, False)
                    else:
                        return (None, False)
                else:
                    return (length, True)
            except PositionOutOfBoardError:
                return (length, True)

    def get_ship_if_whole_sunk(self, position, max_length):
        """Return ship object if ship near or in given position is entirely sunk else return None."""
        first_square = self.get_square(position)
        if first_square == attacked_sea_ind:
            new_position = self.find_nearest_att_ship(position)
            if new_position:
                position = new_position
        row, column = position
        first_square = self.get_square(position)
        n_length, n_ship_sunk = self.one_way_ship_length_is_sunk(position, (-1, 0))
        w_length, w_ship_sunk = self.one_way_ship_length_is_sunk(position, (0, -1))
        s_length, s_ship_sunk = self.one_way_ship_length_is_sunk(position, (1, 0))
        e_length, e_ship_sunk = self.one_way_ship_length_is_sunk(position, (0, 1))
        if n_length is None or w_length is None or s_length is None or e_length is None:
            return None
        elif first_square == attacked_ship_ind:
            if n_length == 0 and w_length == 0 and s_length == 0 and e_length == 0 and max_length == 1:
                return Ship(position, Direction.horizontal, 1)
            elif n_length > 0 or s_length > 0:
                ship_length = n_length + s_length + 1
                ship_position = (row - n_length, column)
                ship = Ship(ship_position, Direction.vertical, ship_length)
                if n_ship_sunk and s_ship_sunk:
                    return ship
                elif ship_length >= max_length:
                    return ship
                else:
                    return None
            elif w_length > 0 or e_length > 0:
                ship_length = w_length + e_length + 1
                ship_position = (row, column - w_length)
                ship = Ship(ship_position, Direction.horizontal, ship_length)
                if w_ship_sunk and e_ship_sunk:
                    return ship
                elif ship_length >= max_length:
                    return ship
                else:
                    return None
            elif n_ship_sunk and w_ship_sunk and s_ship_sunk and e_ship_sunk:
                return Ship(position, Direction.horizontal, 1)
            else:
                return None
        else:
            return None

    def __str__(self):
        """Return string representation of the board."""
        result = '  '
        for number in range(ord('A'), ord('A') + self._size):
            result = result + ' ' + chr(number)
        result = result + '\n'
        for index, row in enumerate(self._board):
            if index >= 9:
                result = result + str(index + 1)
            else:
                result = result + ' ' + str(index + 1)
            for square in row:
                result = result + ' ' + square
            result = result + '\n'
        return result
