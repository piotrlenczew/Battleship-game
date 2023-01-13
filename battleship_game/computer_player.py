from ship import Ship
from battleshipboard import BattleshipBoard, CanNotPlaceShipError
from random import randint
from square_indications import sea_ind, ship_ind, attacked_sea_ind, attacked_ship_ind
from player import generate_position, generate_ship, remove_ship_length_from_list_of_lengths





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
        player_board.set_squares_around_ship(ship, attacked_sea_ind)
        self._list_of_ship_lengths = remove_ship_length_from_list_of_lengths(length, self._list_of_ship_lengths)
        if self._list_of_ship_lengths:
            self._current_max_length = max(self._list_of_ship_lengths)

    def north_targetted_ship(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the north
        - square to the north ,target is ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_ship_ind)
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
        - square to the north, target is sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_sea_ind)
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
        - square to the north, target is attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_sea_ind)
        if self._computer_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
            square = player_board.get_square((first_hit_row + 1, first_hit_column))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'v'
                if player_board.get_square(self._target) == ship_ind:
                    self.south_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.south_targetted_sea(player_board)
                else:
                    self.south_targetted_attacked_sea(player_board)
            elif square == sea_ind:
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
        - first square to the north, target is sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, attacked_sea_ind)
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
        - first square to the north, target is attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, attacked_sea_ind)
        if player_board.position_in_board((first_hit_row, first_hit_column - 1)):
            self._direction_of_guessing = 'w'
            self._target = (first_hit_row, first_hit_column - 1)
            square = player_board.get_square((first_hit_row, first_hit_column - 1))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'h'
                if player_board.get_square(self._target) == ship_ind:
                    self.west_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.west_targetted_sea(player_board)
                else:
                    self.west_targetted_attacked_sea(player_board)
            elif square == sea_ind:
                self.west_no_ship(player_board)
            else:
                self.west_no_ship_checked(player_board)
        elif player_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
            square = player_board.get_square((first_hit_row + 1, first_hit_column))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'v'
                if player_board.get_square(self._target) == ship_ind:
                    self.south_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.south_targetted_sea(player_board)
                else:
                    self.south_targetted_attacked_sea(player_board)
            elif square == sea_ind:
                self.south_no_ship(player_board)
            else:
                self.south_no_ship_checked(player_board)
        else:
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'h'
                if player_board.get_square(self._target) == ship_ind:
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == sea_ind:
                self.east_no_ship(player_board)
            else:
                self.east_no_ship_checked(player_board)

    def west_targetted_ship(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the west
        - square to the west ,target is ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_ship_ind)
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
        - square to the west, target is sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_sea_ind)
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
        - square to the west, target is attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_sea_ind)
        self._targetted_ship_first_position = (row, column + 1)
        if self._computer_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'h'
                if player_board.get_square(self._target) == ship_ind:
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == sea_ind:
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
        - first square to the west, target is sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, attacked_sea_ind)
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
        - first square to the west, target is attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, attacked_sea_ind)
        if player_board.position_in_board((first_hit_row + 1, first_hit_column)):
            self._direction_of_guessing = 's'
            self._target = (first_hit_row + 1, first_hit_column)
            square = player_board.get_square((first_hit_row + 1, first_hit_column))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'v'
                if player_board.get_square(self._target) == ship_ind:
                    self.south_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.south_targetted_sea(player_board)
                else:
                    self.south_targetted_attacked_sea(player_board)
            elif square == sea_ind:
                self.south_no_ship(player_board)
            else:
                self.south_no_ship_checked(player_board)
        elif player_board.position_in_board((first_hit_row, first_hit_column + 1)):
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'h'
                if player_board.get_square(self._target) == ship_ind:
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == sea_ind:
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
        - square to the south ,target is ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_ship_ind)
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
        - square to the south, target is sea
        """
        player_board.set_square(self._target, attacked_sea_ind)
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()

    def south_targetted_attacked_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in vertical position
        - we are searching to the south
        - square to the south, target is attacked_sea
        """
        player_board.set_square(self._target, attacked_sea_ind)
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
        - first square to the south, target is sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, attacked_sea_ind)
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
        - first square to the south, target is attacked_sea
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        player_board.set_square(self._target, attacked_sea_ind)
        if player_board.position_in_board((first_hit_row, first_hit_column + 1)) and self._targetted_ship_first_position == self._first_ship_hit:
            self._direction_of_guessing = 'e'
            self._target = (first_hit_row, first_hit_column + 1)
            square = player_board.get_square((first_hit_row, first_hit_column + 1))
            if square == ship_ind or square == attacked_ship_ind:
                self._targetted_ship_direction = 'h'
                if player_board.get_square(self._target) == ship_ind:
                    self.east_targetted_ship(player_board)
                elif player_board.get_square(self._target) == sea_ind:
                    self.east_targetted_sea(player_board)
                else:
                    self.east_targetted_attacked_sea(player_board)
            elif square == sea_ind:
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
        - square to the east, target is ship
        """
        first_hit_row, first_hit_column = self._first_ship_hit
        row, column = self._target
        player_board.set_square(self._target, attacked_ship_ind)
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
        - square to the east, target is sea
        """
        player_board.set_square(self._target, attacked_sea_ind)
        if not self._targetted_ship_first_position:
            self._targetted_ship_first_position = self._first_ship_hit
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()

    def east_targetted_attacked_sea(self, player_board):
        """
        What to do when:
        - we know that ship is in horizontal position
        - we are searching to the east
        - square to the east, target is attacked_sea
        """
        player_board.set_square(self._target, attacked_sea_ind)
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
        - first square to the east, target is sea
        """
        player_board.set_square(self._target, attacked_sea_ind)
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()

    def east_no_ship_checked(self, player_board):
        """
        What to do when:
        - we don't know that ship is in vertical position
        - we are searching to the east
        - first square to the east, target is attacked_sea
        """
        player_board.set_square(self._target, attacked_sea_ind)
        self.whole_ship_found(player_board)
        self.reset_targetted_ship()
        self.guess(player_board)

    def guess(self, player_board):
        if not self._target:
            while True:
                position = generate_position(self._computer_board.size())
                square = player_board.get_square(position)
                row, column = position
                if square == ship_ind:
                    self._first_ship_hit = position
                    self._targetted_ship_first_position = position
                    player_board.set_square(position, attacked_ship_ind)
                    self._targetted_ship_length = 1
                    if self._computer_board.position_in_board((row - 1, column)):
                        self._targetted_ship_direction = 'v'
                        self._direction_of_guessing = 'n'
                        self._target = (row - 1, column)
                        return
                    elif self._computer_board.position_in_board((row, column - 1)):
                        self._targetted_ship_direction = 'h'
                        self._direction_of_guessing = 'w'
                        self._target = (row, column - 1)
                        return
                    else:
                        self._targetted_ship_direction = 'v'
                        self._direction_of_guessing = 's'
                        self._target = (row + 1, column)
                        return
                elif square == sea_ind:
                    player_board.set_square(position, attacked_sea_ind)
                    self.reset_targetted_ship()
                    return
                else:
                    pass
        else:
            first_hit_row, first_hit_column = self._first_ship_hit
            if self._direction_of_guessing == 'n':
                square = player_board.get_square((first_hit_row - 1, first_hit_column))
                if square == ship_ind or square == attacked_ship_ind:
                    self._targetted_ship_direction = 'v'
                    if player_board.get_square(self._target) == ship_ind:
                        self.north_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == sea_ind:
                        self.north_targetted_sea(player_board)
                    else:
                        self.north_targetted_attacked_sea(player_board)
                elif square == sea_ind:
                    self.north_no_ship(player_board)
                else:
                    self.north_no_ship_checked(player_board)
            elif self._direction_of_guessing == 'w':
                square = player_board.get_square((first_hit_row, first_hit_column - 1))
                if square == ship_ind or square == attacked_ship_ind:
                    self._targetted_ship_direction = 'h'
                    if player_board.get_square(self._target) == ship_ind:
                        self.west_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == sea_ind:
                        self.west_targetted_sea(player_board)
                    else:
                        self.west_targetted_attacked_sea(player_board)
                elif square == sea_ind:
                    self.west_no_ship(player_board)
                else:
                    self.west_no_ship_checked(player_board)
            elif self._direction_of_guessing == 's':
                square = player_board.get_square((first_hit_row + 1, first_hit_column))
                if square == ship_ind or square == attacked_ship_ind:
                    self._targetted_ship_direction = 'v'
                    if player_board.get_square(self._target) == ship_ind:
                        self.south_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == sea_ind:
                        self.south_targetted_sea(player_board)
                    else:
                        self.south_targetted_attacked_sea(player_board)
                elif square == sea_ind:
                    self.south_no_ship(player_board)
                else:
                    self.south_no_ship_checked(player_board)
            else:
                square = player_board.get_square((first_hit_row, first_hit_column + 1))
                if square == ship_ind or square == attacked_ship_ind:
                    self._targetted_ship_direction = 'h'
                    if player_board.get_square(self._target) == ship_ind:
                        self.east_targetted_ship(player_board)
                    elif player_board.get_square(self._target) == sea_ind:
                        self.east_targetted_sea(player_board)
                    else:
                        self.east_targetted_attacked_sea(player_board)
                elif square == sea_ind:
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
