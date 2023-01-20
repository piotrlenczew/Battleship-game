from game_files.defined_enumerations import Direction, Course


class IncorrectPositionError(Exception):
    """Inappropriate position."""
    pass


class IncorrectSizeError(Exception):
    """Inappropriate size."""
    pass


class IncorrectDirectionError(Exception):
    """Inappropriate direction."""
    pass


class IncorrectLengthOfShipError(Exception):
    """Inappropriate length."""
    pass


class NoSuchCourseError(Exception):
    """Inappropriate course."""
    pass


class Ship:
    """
    Class Ship. Contains attributes:
    :parametr position: tuple made up of two intigers indicating row and column
    :type position: tuple

    :param direction: can only be vertical or horizontal
    :type direction: str

    :param length: number of squares that form ship
    :type length: int
    """
    def __init__(self, position, direction, length):
        """Initialize instance os Ship."""
        try:
            if len(position) != 2:
                raise IncorrectPositionError('More than 2 dimensions given')
        except TypeError:
            raise IncorrectPositionError('Only one dimension given')
        self._position = position
        if direction != Direction.vertical and direction != Direction.horizontal:
            message = f'Directions can only be: {Direction.vertical} - vertical or {Direction.horizontal} - horizontal'
            raise IncorrectDirectionError(message)
        self._direction = direction
        if length < 1:
            raise IncorrectLengthOfShipError('Ship must have positive length')
        self._length = length

    def position(self):
        """Get position attribute."""
        return self._position

    def direction(self):
        """Get direction attribute."""
        return self._direction

    def length(self):
        """Get length attribute."""
        return self._length

    def fits_in_board(self, size):
        """Check if the ship fits in board of given size."""
        if size <= 0:
            raise IncorrectSizeError('Size needs to be positive')
        row, column = self._position
        if row < 0 or column < 0:
            return False
        if self._direction == Direction.vertical:
            if row + self._length > size:
                return False
        else:
            if column + self._length > size:
                return False
        return True

    def positions(self):
        """Return a list of square positions that form the ship"""
        row, column = self._position
        result = []
        if self._direction == Direction.vertical:
            for addend in range(self._length):
                result.append((row + addend, column))
        else:
            for addend in range(self._length):
                result.append((row, column + addend))
        return result

    def move_ship(self, course, board_size):
        """Move given ship to given course by 1 square if able."""
        position = self.position()
        row, column = position
        if course == Course.north:
            if row - 1 < 0:
                new_position = position
            else:
                new_position = (row - 1, column)
        elif course == Course.west:
            if column - 1 < 0:
                new_position = position
            else:
                new_position = (row, column - 1)
        elif course == Course.south:
            if self._direction == Direction.vertical:
                if row + self._length >= board_size:
                    new_position = position
                else:
                    new_position = (row + 1, column)
            else:
                if row + 1 >= board_size:
                    new_position = position
                else:
                    new_position = (row + 1, column)
        elif course == Course.east:
            if self._direction == Direction.horizontal:
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
            raise NoSuchCourseError(f'Course can only be: {Course.north} - north, {Course.west} - west, {Course.south} - south or {Course.east} - east')
        self._position = new_position

    def rotate_ship(self, board_size):
        """Rotate ship if able"""
        direction = self.direction()
        if direction == Direction.horizontal:
            new_direction = Direction.vertical
        else:
            new_direction = Direction.horizontal
        new_ship = Ship(self.position(), new_direction, self.length())
        if new_ship.fits_in_board(board_size):
            self._direction = new_direction

    def __bool__(self):
        return True
