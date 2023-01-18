from ship import Ship
from battleshipboard import BattleshipBoard, CanNotPlaceShipError
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

    def guess(self, player_board):
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
                direction = self._direction_of_guessing
                if direction == 'n' or direction == 's':
                    self._targetted_ship_direction = 'v'
                elif direction == 'w' or direction == 'e':
                    self._targetted_ship_direction = 'h'
                self.targetted_ship(player_board)
            elif square == sea_ind:
                self.targetted_sea(player_board)
            elif square == attacked_sea_ind:
                self.targetted_attacked_sea(player_board)

    def place_ship(self, length):
        while True:
            try:
                ship = generate_ship(length, self._computer_board.size())
                self._computer_board.place_ship(ship)
                return
            except CanNotPlaceShipError:
                pass

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
        if not direction:
            direction = 'v'
        length = self._targetted_ship_length
        ship = Ship(position, direction, length)
        player_board.set_squares_around_ship(ship, attacked_sea_ind)
        self._list_of_ship_lengths = remove_ship_length_from_list_of_lengths(length, self._list_of_ship_lengths)
        if self._list_of_ship_lengths:
            self._current_max_length = max(self._list_of_ship_lengths)

    def ship_found(self, player_board):
        player_board.set_square(self._target, attacked_ship_ind)
        direction = self._direction_of_guessing
        if direction == 'n' or direction == 'w':
            self._targetted_ship_first_position = self._target
        self._targetted_ship_length += 1

    def targetted_ship(self, player_board):
        self.ship_found(player_board)
        if self._targetted_ship_length >= self._current_max_length:
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
        elif not self.find_new_target_in_board(player_board, self._target, True):
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def targetted_sea(self, player_board):
        player_board.set_square(self._target, attacked_sea_ind)
        if not self.find_new_target_in_board(player_board, self._target, False):
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()

    def targetted_attacked_sea(self, player_board):
        if not self.find_new_target_in_board(player_board, self._target, False):
            self.whole_ship_found(player_board)
            self.reset_targetted_ship()
        self.guess(player_board)

    def find_new_target_in_board(self, player_board, current_position, is_targetted_ship):
        row, column = current_position
        first_row, first_column = self._first_ship_hit
        direction = self._direction_of_guessing
        n_in_board = player_board.position_in_board((row - 1, column))
        w_in_board = player_board.position_in_board((row, column - 1))
        s_in_board = player_board.position_in_board((row + 1, column))
        e_in_board = player_board.position_in_board((row, column + 1))
        first_w_in_board = player_board.position_in_board((first_row, first_column - 1))
        first_s_in_board = player_board.position_in_board((first_row + 1, first_column))
        first_e_in_board = player_board.position_in_board((first_row, first_column + 1))
        if not direction:
            if n_in_board:
                self._direction_of_guessing = 'n'
                self._target = (row - 1, column)
                return True
            elif w_in_board:
                self._direction_of_guessing = 'w'
                self._target = (row, column - 1)
                return True
            elif s_in_board:
                self._direction_of_guessing = 's'
                self._target = (row + 1, column)
                return True
            elif e_in_board:
                self._direction_of_guessing = 'e'
                self._target = (row, column + 1)
                return True
            else:
                return False
        elif direction == 'n':
            if self._targetted_ship_direction == 'v':
                if n_in_board and is_targetted_ship:
                    self._target = (row - 1, column)
                    return True
                elif first_s_in_board:
                    self._direction_of_guessing = 's'
                    self._target = (first_row + 1, first_column)
                    return True
                else:
                    return False
            else:
                if n_in_board and is_targetted_ship:
                    self._target = (row - 1, column)
                    return True
                elif first_w_in_board:
                    self._direction_of_guessing = 'w'
                    self._target = (first_row, first_column - 1)
                    return True
                elif first_s_in_board:
                    self._direction_of_guessing = 's'
                    self._target = (first_row + 1, first_column)
                    return True
                elif first_e_in_board:
                    self._direction_of_guessing = 'e'
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
        elif direction == 'w':
            if self._targetted_ship_direction == 'h':
                if w_in_board and is_targetted_ship:
                    self._target = (row, column - 1)
                    return True
                elif first_e_in_board:
                    self._direction_of_guessing = 'e'
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
            else:
                if w_in_board and is_targetted_ship:
                    self._target = (row, column - 1)
                    return True
                elif first_s_in_board:
                    self._direction_of_guessing = 's'
                    self._target = (first_row + 1, first_column)
                    return True
                elif first_e_in_board:
                    self._direction_of_guessing = 'e'
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
        elif direction == 's':
            if self._targetted_ship_direction == 'v':
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
                    self._direction_of_guessing = 'e'
                    self._target = (first_row, first_column + 1)
                    return True
                else:
                    return False
        elif direction == 'e':
            if e_in_board and is_targetted_ship:
                self._target = (row, column + 1)
                return True
            else:
                return False
