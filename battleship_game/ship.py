class IncorrectPositionError(Exception):
    pass


class IncorrectSizeError(Exception):
    pass


class IncorrectDirectionError(Exception):
    pass


class IncorrectLengthOfShipError(Exception):
    pass


class NoSuchCourseError(Exception):
    pass


class Ship:
    """
    Class Ship. Contains attributes:
    :parametr position: tuple made up of two intigers indicating row and column
    :type position: tuple

    :param direction: can only be v - vertical or h - horizontal
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
        if direction != 'v' and direction != 'h':
            message = 'Directions can only be: v - vertical or h - horizontal'
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
        if row < 0 or column < 0:
            return False
        if self._direction == 'v':
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
        if self._direction == 'v':
            for addend in range(self._length):
                result.append((row + addend, column))
        else:
            for addend in range(self._length):
                result.append((row, column + addend))
        return result

    def move_ship(self, course, board_size):
        """
        Moves given ship to given course by 1 square if able
        """
        position = self.position()
        row, column = position
        if course == 'n':
            if row - 1 < 0:
                new_position = position
            else:
                new_position = (row - 1, column)
        elif course == 'w':
            if column - 1 < 0:
                new_position = position
            else:
                new_position = (row, column - 1)
        elif course == 's':
            if self._direction == 'v':
                if row + self._length >= board_size:
                    new_position = position
                else:
                    new_position = (row + 1, column)
            else:
                if row + 1 >= board_size:
                    new_position = position
                else:
                    new_position = (row + 1, column)
        elif course == 'e':
            if self._direction == 'h':
                if column + self._length >= board_size:
                    new_position = position
                else:
                    new_position = (row, column + 1)
            else:
                if column + 1 >= board_size:
                    new_position = position
                else:
                    new_position = (row, column + 1)
        else:
            raise NoSuchCourseError('Course can only be: [n/w/e/s]')
        self._position = new_position



    def rotate_ship(self, board_size):
        """
        Rotates ship if able
        """
        direction = self.direction()
        if direction == 'h':
            new_direction = 'v'
        else:
            new_direction = 'h'
        new_ship = Ship(self.position(), new_direction, self.length())
        if new_ship.fits_in_board(board_size):
            self._direction = new_direction

    def __bool__(self):
        return True
