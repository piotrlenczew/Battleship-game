from game_files.defined_enumerations import Direction, Course
from game_files.ship import Ship
from game_files.battleshipboard import BattleshipBoard, CanNotPlaceShipError
from game_files.game_settings import (
    sea_ind, ship_ind, attacked_sea_ind, attacked_ship_ind
)
from game_files.player import (
    generate_position, generate_ship, remove_ship_length_from_list_of_lengths
)


class ComputerPlayer():
    """
    Class ComputerPlayer. Contains attributes:
    :param computer_board: a board where computer places it's ships
    :type computer_board: BattleshiBoard

    :param list_of_ships_lentgh: list of length of ships that will be placed
    :type list_of_ships_length: list
    """
    def __init__(self, board_size, list_of_ships_length):
        """Initialize instance of ComputerPlayer"""
        self._computer_board = BattleshipBoard(board_size)
        list_of_ships_length.sort()
        self._list_of_ships_length = list_of_ships_length
        self._current_max_length = max(list_of_ships_length)
        self._first_ship_hit = None
        self._target = None
        self._course_of_guessing = None
        self._targetted_ship_first_position = None
        self._targetted_ship_length = None
        self._targetted_ship_direction = None

    def computer_board(self):
        """Get computer_board attribute."""
        return self._computer_board

    def list_of_ships_length(self):
        """Get list_of_ships_length attribute."""
        return self._list_of_ships_length

    def guess(self, player_board):
        """
        Guess one square.

        - If previous square was't ship guess random square
        - Else search anticlockwise from last guess for valid guess target
        - If whole ship found set squares around to attacked_sea_ind
        """
        if not self._target:
            while True:
                position = generate_position(self._computer_board.size())
                square = player_board.get_square(position)
                if square == ship_ind:
                    self._first_ship_hit = position
                    self._targetted_ship_first_position = position
                    player_board.set_square(position, attacked_ship_ind)
                    self._targetted_ship_length = 1
                    if self._current_max_length == 1:
                        self.whole_ship_found(player_board)
                        self.reset_targetted_ship()
                        return
                    elif self.find_new_target_in_board(player_board, position, True):
                        return
                    else:
                        self.whole_ship_found(player_board)
                        self.reset_targetted_ship()
                        return
                elif square == sea_ind:
                    player_board.set_square(position, attacked_sea_ind)
                    self.reset_targetted_ship()
                    return
        else:
            square = player_board.get_square(self._target)
            if square == ship_ind:
                course = self._course_of_guessing
                if course == Course.north or course == Course.south:
                    self._targetted_ship_direction = Direction.vertical
                elif course == Course.west or course == Course.east:
                    self._targetted_ship_direction = Direction.horizontal
                self.targetted_ship(player_board)
            elif square == sea_ind:
                self.targetted_sea(player_board)
            elif square == attacked_sea_ind:
                self.targetted_attacked_sea(player_board)

    def place_ship(self, length):
        """Place random ship of given length."""
        while True:
            try:
                ship = generate_ship(length, self._computer_board.size())
                self._computer_board.place_ship(ship)
                return
            except CanNotPlaceShipError:
                pass

    def reset_targetted_ship(self):
        """Reset search data."""
        self._first_ship_hit = None
        self._target = None
        self._course_of_guessing = None
        self._targetted_ship_first_position = None
        self._targetted_ship_length = None
        self._targetted_ship_direction = None

    def whole_ship_found(self, player_board):
        """
        What to do when whole ship found.

        - Create ship based on search data
        - Call set_squares_around_ship method
        - Update list_of_ships_length and current_max_length
        """
        position = self._targetted_ship_first_position
        direction = self._targetted_ship_direction
        if not direction:
            direction = Direction.vertical
        length = self._targetted_ship_length
        ship = Ship(position, direction, length)
        player_board.set_squares_around_ship(ship, attacked_sea_ind)
        self._list_of_ships_length = remove_ship_length_from_list_of_lengths(length, self._list_of_ships_length)
        if self._list_of_ships_length:
            self._current_max_length = max(self._list_of_ships_length)

    def ship_found(self, player_board):
        """
        What to do when ship square found.

        - Set square to attacked_ship_ind
        - Change targetted_ship_first_position if course is north or west
        - Increment targetted_ship_length
        """
        player_board.set_square(self._target, attacked_ship_ind)
        course = self._course_of_guessing
        if course == Course.north or course == Course.west:
            self._targetted_ship_first_position = self._target
        self._targetted_ship_length += 1

    def targetted_ship(self, player_board):
        """
        What to do when ship targetted.

        - Call ship_found method
        - If ship length is max call whole_ship_found and reset_targetted_ship methods
        - Find new target and if find_new_target_in_board returns True, call whole_ship_found and reset_targetted_ship methods
        """
        self.ship_found(player_board)
        if self._targetted_ship_length >= self._current_max_length:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
        elif not self.find_new_target_in_board(player_board, self._target, True):
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def targetted_sea(self, player_board):
        """
        What to do when sea targetted.

        - Set square to attacked_sea_ind
        - Find new target and if find_new_target_in_board returns True, call whole_ship_found and reset_targetted_ship methods
        """
        player_board.set_square(self._target, attacked_sea_ind)
        if not self.find_new_target_in_board(player_board, self._target, False):
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def targetted_attacked_sea(self, player_board):
        """
        What to do when attacked_sea_targeted.

        - Find new target and if find_new_target_in_board returns True, call whole_ship_found and reset_targetted_ship methods
        - Call guess method
        """
        if not self.find_new_target_in_board(player_board, self._target, False):
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
        self.guess(player_board)

    def find_new_target_in_board(self, player_board, current_position, is_targetted_ship):
        """
        Finds new target based on search data, current_position and is_targetted_ship.

        search data:
        - first_ship_hit
        - target
        - course_of_guessing
        - targetted_ship_first_position
        - targetted_ship_length
        - targetted_ship_direction
        current_position - targetted position before method used
        is_targetted_ship - bool variable that indicates if square in current_position is ship_ ind
        """
        row, column = current_position
        first_row, first_column = self._first_ship_hit
        course = self._course_of_guessing
        n_in_board = player_board.position_in_board((row - 1, column))
        w_in_board = player_board.position_in_board((row, column - 1))
        s_in_board = player_board.position_in_board((row + 1, column))
        e_in_board = player_board.position_in_board((row, column + 1))
        first_w_in_board = player_board.position_in_board((first_row, first_column - 1))
        first_s_in_board = player_board.position_in_board((first_row + 1, first_column))
        first_e_in_board = player_board.position_in_board((first_row, first_column + 1))
        if not course:
            if n_in_board:
                self._course_of_guessing = Course.north
                self._target = (row - 1, column)
                return True
            elif w_in_board:
                self._course_of_guessing = Course.west
                self._target = (row, column - 1)
                return True
            elif s_in_board:
                self._course_of_guessing = Course.south
                self._target = (row + 1, column)
                return True
            elif e_in_board:
                self._course_of_guessing = Course.east
                self._target = (row, column + 1)
                return True
            else:
                return False
        elif course == Course.north:
            if self._targetted_ship_direction == Direction.vertical:
                if n_in_board and is_targetted_ship:
                    self._target = (row - 1, column)
                    return True
                elif first_s_in_board:
                    self._course_of_guessing = Course.south
                    self._target = (first_row + 1, first_column)
                    return True
                else:
                    return False
            else:
                if n_in_board and is_targetted_ship:
                    self._target = (row - 1, column)
                    return True
                elif first_w_in_board:
                    self._course_of_guessing = Course.west
                    self._target = (first_row, first_column - 1)
                    return True
                elif first_s_in_board:
                    self._course_of_guessing = Course.south
                    self._target = (first_row + 1, first_column)
                    return True
                elif first_e_in_board:
                    self._course_of_guessing = Course.east
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
        elif course == Course.west:
            if self._targetted_ship_direction == Direction.horizontal:
                if w_in_board and is_targetted_ship:
                    self._target = (row, column - 1)
                    return True
                elif first_e_in_board:
                    self._course_of_guessing = Course.east
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
            else:
                if w_in_board and is_targetted_ship:
                    self._target = (row, column - 1)
                    return True
                elif first_s_in_board:
                    self._course_of_guessing = Course.south
                    self._target = (first_row + 1, first_column)
                    return True
                elif first_e_in_board:
                    self._course_of_guessing = Course.east
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
        elif course == Course.south:
            if self._targetted_ship_direction == Direction.vertical:
                if s_in_board and is_targetted_ship:
                    self._target = (row + 1, column)
                    return True
                else:
                    return False
            else:
                if s_in_board and is_targetted_ship:
                    self._target = (row + 1, column)
                    return True
                elif first_e_in_board:
                    self._course_of_guessing = Course.east
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
        elif course == Course.east:
            if e_in_board and is_targetted_ship:
                self._target = (row, column + 1)
                return True
            else:
                return False
