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


class NegativeDimensionError(Exception):
    pass


# s - South, e - East
class Ship:
    """
    Class Ship. Contains attributes:
    :parametr position: tuple made up of two intigers indicating row and column
    :type position: tuple

    :param direction: can only be s - South, e - East, n - north, w - west
    :type direction: str

    :param length: number of squares that form ship
    :type length: int
    """
    def __init__(self, position, direction, length):
        if type(position) is int:
            raise IncorrectPositionError('1 dimension given')
        if len(position) != 2:
            raise IncorrectPositionError('More than 2 dimensions given')
        if direction == 'n':
            row, column = position
            position = (row - length + 1, column)
            direction = 's'
        elif direction == 'w':
            row, column = position
            position = (row, column - length + 1)
            direction = 'e'
        elif direction != 's' and direction != 'e':
            message = 'Directions can only be: s - South, e - East, n - North, w - West'
            raise IncorrectDirectionError(message)
        if length < 1:
            raise IncorrectLengthOfShipError('Ship must have positive length')
        row, column = position
        if row < 0 or column < 0:
            raise NegativeDimensionError('At least one position has negative dimension')
        self._direction = direction
        self._position = position
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

    def position_in_board(self, position):
        """
        Checks if position is in board
        """
        row, column = position
        size = self._size
        if row < 0 or row > size - 1 or column < 0 or column > size - 1:
            return False
        return True

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

    def set_if_in_board(self, position, indication):
        row, column = position
        if row >= 0 and column >= 0 and row < self.size() and column < self.size():
            self.set_square(position, indication)

    def set_squares_around_ship(self, ship, indication):
        position = ship.position()
        row, column = position
        direction = ship.direction()
        length = ship.length()
        if direction == 's':
            self.set_if_in_board((row, column + 1), indication)
            self.set_if_in_board((row - 1, column + 1), indication)
            self.set_if_in_board((row - 1, column), indication)
            self.set_if_in_board((row - 1, column - 1), indication)
            self.set_if_in_board((row, column - 1), indication)
            for number in range(1, length - 1):
                self.set_if_in_board((row + number, column + 1), indication)
                self.set_if_in_board((row + number, column - 1), indication)
            self.set_if_in_board((row + length - 1, column + 1), indication)
            self.set_if_in_board((row + length, column + 1), indication)
            self.set_if_in_board((row + length, column), indication)
            self.set_if_in_board((row + length, column - 1), indication)
            self.set_if_in_board((row + length - 1, column - 1), indication)
        else:
            self.set_if_in_board((row + 1, column), indication)
            self.set_if_in_board((row + 1, column - 1), indication)
            self.set_if_in_board((row, column - 1), indication)
            self.set_if_in_board((row - 1, column - 1), indication)
            self.set_if_in_board((row - 1, column), indication)
            for number in range(1, length - 1):
                self.set_if_in_board((row + 1, column + number), indication)
                self.set_if_in_board((row - 1, column + number), indication)
            self.set_if_in_board((row + 1, column + length - 1), indication)
            self.set_if_in_board((row + 1, column + length), indication)
            self.set_if_in_board((row, column + length), indication)
            self.set_if_in_board((row - 1, column + length), indication)
            self.set_if_in_board((row - 1, column + length - 1), indication)

    def __str__(self):
        """
        Returns string representation of the board
        """
        result = '  '
        for number in range(ord('A'), ord('K')):
            result = result + ' ' + chr(number)
        result = result + '\n'
        for index, row in enumerate(self._board):
            if index == 9:
                result = result + str(index + 1)
            else:
                result = result + ' ' + str(index + 1)
            for square in row:
                result = result + ' ' + square
            result = result + '\n'
        return result


class Player():
    def __init__(self, board_size):
        self._player_board = BattleshipBoard(board_size)
        self._player_guess_board = BattleshipBoard(board_size)

    def player_board(self):
        return self._player_board

    def player_guess_board(self):
        return self._player_guess_board

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


def generate_position(board_size):
    row = randint(0, board_size - 1)
    column = randint(0, board_size - 1)
    return (row, column)


def generate_ship(length, board_size):
    position = generate_position(board_size)
    condition = randint(0, 1)
    if condition == 0:
        direction = 's'
    else:
        direction = 'e'
    ship = Ship(position, direction, length)
    return ship


def remove_ship_length_from_list_of_lengths(ship_length, list_of_ship_lengths):
    result = []
    found_one = False
    for length in list_of_ship_lengths:
        if length != ship_length:
            result.append(length)
        elif found_one:
            result.append(length)
        else:
            found_one = True
    return result


class ComputerPlayer():
    def __init__(self, board_size, list_of_ships_length):
        self._computer_board = BattleshipBoard(board_size)
        list_of_ships_length.sort()
        self._list_of_ship_lengths = list_of_ships_length
        self._current_max_length = max(list_of_ships_length)
        self._first_ship_hit = None
        self._target = None
        self._direction_of_guessing = None
        self._targetted_ship_first_position = None
        self._targetted_ship_length = None
        self._targetted_ship_direction = None

    def computer_board(self):
        return self._computer_board

    def reset_targetted_ship(self):
        self._first_ship_hit = None
        self._target = None
        self._direction_of_guessing = None
        self._targetted_ship_first_position = None
        self._targetted_ship_length = None
        self._targetted_ship_direction = None

    def whole_ship_found(self, player_board):
        """
        What to do when we found whole ship
        """
        position = self._targetted_ship_first_position
        direction = self._targetted_ship_direction
        length = self._targetted_ship_length
        ship = Ship(position, direction, length)
        player_board.set_squares_around_ship(ship, '~')
        self._list_of_ship_lengths = remove_ship_length_from_list_of_lengths(length, self._list_of_ship_lengths)
        if self._list_of_ship_lengths:
            self._current_max_length = max(self._list_of_ship_lengths)

    def north_targetted_ship(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the north
        - square to the north ,target is 'O' - ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, 'X')
        self._targetted_ship_first_position = self._target
        self._targetted_ship_length += 1
        if self._targetted_ship_length >= self._current_max_length:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            new_list_of_ship_lengths = self._list_of_ship_lengths[:-1]
            self._list_of_ship_lengths = new_list_of_ship_lengths
        elif self._computer_board.position_in_board((row - 1, column)):
            self._target = (row - 1, column)
        elif self._computer_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()


    def north_targetted_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the north
        - square to the north, target is ' ' - sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, '~')
        if self._computer_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def north_targetted_attacked_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the north
        - square to the north, target is '~' - attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, '~')
        if self._computer_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
            square = player_board.get_square((first_hit_row + 1, first_hit_column))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 's'
                if player_board.get_square(self._target) == 'O':
                    self.south_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.south_targetted_sea(player_board)
                else:
                    self.south_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.south_no_ship(player_board)
            else:
                self.south_no_ship_checked(player_board)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            self.guess(player_board)

    def north_no_ship(self, player_board):
        """
        What to do when:
        - we don't know that ship is in vertical position
        - we are searching to the north
        - first square to the north, target is ' ' - sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, '~')
        if player_board.position_in_board((first_hit_row, first_hit_column - 1)):
            self._direction_of_guessing = 'w'
            self._target = (first_hit_row, first_hit_column - 1)
        elif player_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
        else:
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)

    def north_no_ship_checked(self, player_board):
        """
        What to do when:
        - we don't know that ship is in vertical position
        - we are searching to the north
        - first square to the north, target is '~' - attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, '~')
        if player_board.position_in_board((first_hit_row, first_hit_column - 1)):
            self._direction_of_guessing = 'w'
            self._target = (first_hit_row, first_hit_column - 1)
            square = player_board.get_square((first_hit_row, first_hit_column - 1))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 'e'
                if player_board.get_square(self._target) == 'O':
                    self.west_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.west_targetted_sea(player_board)
                else:
                    self.west_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.west_no_ship(player_board)
            else:
                self.west_no_ship_checked(player_board)
        elif player_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
            square = player_board.get_square((first_hit_row + 1, first_hit_column))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 's'
                if player_board.get_square(self._target) == 'O':
                    self.south_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.south_targetted_sea(player_board)
                else:
                    self.south_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.south_no_ship(player_board)
            else:
                self.south_no_ship_checked(player_board)
        else:
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 'e'
                if player_board.get_square(self._target) == 'O':
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.east_no_ship(player_board)
            else:
                self.east_no_ship_checked(player_board)

    def west_targetted_ship(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the west
        - square to the west ,target is 'O' - ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, 'X')
        self._targetted_ship_length += 1
        self._targetted_ship_first_position = self._target
        if self._targetted_ship_length >= self._current_max_length:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            new_list_of_ship_lengths = self._list_of_ship_lengths[:-1]
            self._list_of_ship_lengths = new_list_of_ship_lengths
        elif self._computer_board.position_in_board((row, column - 1)):
            self._target = (row, column - 1)
        elif self._computer_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def west_targetted_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the west
        - square to the west, target is ' ' - sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, '~')
        if self._computer_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def west_targetted_attacked_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the west
        - square to the west, target is '~' - attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, '~')
        self._targetted_ship_first_position = (row, column + 1)
        if self._computer_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 'e'
                if player_board.get_square(self._target) == 'O':
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.east_no_ship(player_board)
            else:
                self.east_no_ship_checked(player_board)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            self.guess(player_board)

    def west_no_ship(self, player_board):
        """
        What to do when:
        - we don't know that ship is in horizontal position
        - we are searching to the west
        - first square to the west, target is ' ' - sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, '~')
        if player_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
        elif player_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def west_no_ship_checked(self, player_board):
        """
        What to do when:
        - we don't know that ship is in horizontal position
        - we are searching to the west
        - first square to the west, target is '~' - attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, '~')
        if player_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
            square = player_board.get_square((first_hit_row + 1, first_hit_column))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 's'
                if player_board.get_square(self._target) == 'O':
                    self.south_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.south_targetted_sea(player_board)
                else:
                    self.south_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.south_no_ship(player_board)
            else:
                self.south_no_ship_checked(player_board)
        elif player_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 'e'
                if player_board.get_square(self._target) == 'O':
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.east_no_ship(player_board)
            else:
                self.east_no_ship_checked(player_board)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            self.guess(player_board)

    def south_targetted_ship(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the south
        - square to the south ,target is 'O' - ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, 'X')
        self._targetted_ship_length += 1
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        if self._targetted_ship_length >= self._current_max_length:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            new_list_of_ship_lengths = self._list_of_ship_lengths[:-1]
            self._list_of_ship_lengths = new_list_of_ship_lengths
        elif self._computer_board.position_in_board((row + 1, column)):
            self._target = (row + 1, column)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def south_targetted_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the south
        - square to the south, target is ' ' - sea
        """
        player_board.set_square(self._target, '~')
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()

    def south_targetted_attacked_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the south
        - square to the south, target is '~' - attacked_sea
        """
        player_board.set_square(self._target, '~')
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()
        self.guess(player_board)

    def south_no_ship(self, player_board):
        """
        What to do when:
        - we don't know that ship is in vertical position
        - we are searching to the south
        - first square to the south, target is ' ' - sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, '~')
        if player_board.position_in_board((first_hit_row, first_hit_column + 1)) and self._targetted_ship_first_position == self._first_ship_hit:
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def south_no_ship_checked(self, player_board):
        """
        What to do when:
        - we don't know that ship is in vertical position
        - we are searching to the south
        - first square to the south, target is '~' - attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, '~')
        if player_board.position_in_board((first_hit_row, first_hit_column + 1)) and self._targetted_ship_first_position == self._first_ship_hit:
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == 'O' or square == 'X':
                self._targetted_ship_direction = 'e'
                if player_board.get_square(self._target) == 'O':
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == ' ':
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == ' ':
                self.east_no_ship(player_board)
            else:
                self.east_no_ship_checked(player_board)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            self.guess(player_board)

    def east_targetted_ship(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the east
        - square to the east, target is 'O' - ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, 'X')
        self._targetted_ship_length += 1
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        if self._targetted_ship_length >= self._current_max_length:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
            new_list_of_ship_lengths = self._list_of_ship_lengths[:-1]
            self._list_of_ship_lengths = new_list_of_ship_lengths
        elif self._computer_board.position_in_board((row, column + 1)):
            self._target = (row, column + 1)
        else:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def east_targetted_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the east
        - square to the east, target is ' ' - sea
        """
        player_board.set_square(self._target, '~')
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()

    def east_targetted_attacked_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the east
        - square to the east, target is '~' - attacked_sea
        """
        player_board.set_square(self._target, '~')
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()
        self.guess(player_board)

    def east_no_ship(self, player_board):
        """
        What to do when:
        - we don't know that ship is in horizontal position
        - we are searching to the east
        - first square to the east, target is ' ' - sea
        """
        player_board.set_square(self._target, '~')
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()

    def east_no_ship_checked(self, player_board):
        """
        What to do when:
        - we don't know that ship is in vertical position
        - we are searching to the east
        - first square to the east, target is '~' - attacked_sea
        """
        player_board.set_square(self._target, '~')
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()
        self.guess(player_board)

    def guess(self, player_board):
        if not self._target:
            while True:
                position = generate_position(self._computer_board.size())
                square = player_board.get_square(position)
                row, column = position
                if square == 'O':
                    self._first_ship_hit = position
                    self._targetted_ship_first_position = position
                    player_board.set_square(position, 'X')
                    self._targetted_ship_length = 1
                    if self._computer_board.position_in_board((row - 1, column)):
                        self._targetted_ship_direction = 's'
                        self._direction_of_guessing = 'n'
                        self._target = (row - 1, column)
                        return
                    elif self._computer_board.position_in_board((row, column - 1)):
                        self._targetted_ship_direction = 'e'
                        self._direction_of_guessing = 'w'
                        self._target = (row, column - 1)
                        return
                    else:
                        self._targetted_ship_direction = 's'
                        self._direction_of_guessing = 's'
                        self._target = (row + 1, column)
                        return
                elif square == ' ':
                    player_board.set_square(position, '~')
                    self.reset_targetted_ship()
                    return
                else:
                    pass
        else:
            first_hit_row, first_hit_column = self._first_ship_hit
            if self._direction_of_guessing == 'n':
                square = player_board.get_square((first_hit_row - 1, first_hit_column))
                if square == 'O' or square == 'X':
                    self._targetted_ship_direction = 's'
                    if player_board.get_square(self._target) == 'O':
                        self.north_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == ' ':
                        self.north_targetted_sea(player_board)
                    else:
                        self.north_targetted_attacked_sea(player_board)
                elif square == ' ':
                    self.north_no_ship(player_board)
                else:
                    self.north_no_ship_checked(player_board)
            elif self._direction_of_guessing == 'w':
                square = player_board.get_square((first_hit_row, first_hit_column - 1))
                if square == 'O' or square == 'X':
                    self._targetted_ship_direction = 'e'
                    if player_board.get_square(self._target) == 'O':
                        self.west_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == ' ':
                        self.west_targetted_sea(player_board)
                    else:
                        self.west_targetted_attacked_sea(player_board)
                elif square == ' ':
                    self.west_no_ship(player_board)
                else:
                    self.west_no_ship_checked(player_board)
            elif self._direction_of_guessing == 's':
                square = player_board.get_square((first_hit_row + 1, first_hit_column))
                if square == 'O' or square == 'X':
                    self._targetted_ship_direction = 's'
                    if player_board.get_square(self._target) == 'O':
                        self.south_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == ' ':
                        self.south_targetted_sea(player_board)
                    else:
                        self.south_targetted_attacked_sea(player_board)
                elif square == ' ':
                    self.south_no_ship(player_board)
                else:
                    self.south_no_ship_checked(player_board)
            else:
                square = player_board.get_square((first_hit_row, first_hit_column + 1))
                if square == 'O' or square == 'X':
                    self._targetted_ship_direction = 'e'
                    if player_board.get_square(self._target) == 'O':
                        self.east_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == ' ':
                        self.east_targetted_sea(player_board)
                    else:
                        self.east_targetted_attacked_sea(player_board)
                elif square == ' ':
                    self.east_no_ship(player_board)
                else:
                    self.east_no_ship_checked(player_board)

    def place_ship(self, length):
        while True:
            try:
                ship = generate_ship(length, self._computer_board.size())
                self._computer_board.place_ship(ship)
                return
            except CanNotPlaceShipError:
                pass
