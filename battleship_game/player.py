from ship import Ship, NoSuchCourseError
from battleshipboard import BattleshipBoard, CanNotPlaceShipError
from random import randint
from square_indications import sea_ind, ship_ind, attacked_sea_ind, attacked_ship_ind


def generate_position(board_size):
    row = randint(0, board_size - 1)
    column = randint(0, board_size - 1)
    return (row, column)


def generate_ship(length, board_size):
    position = generate_position(board_size)
    condition = randint(0, 1)
    if condition == 0:
        direction = 'v'
    else:
        direction = 'h'
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


class Player():
    """
    Class Player. Contains attributes:
    :parametr player_board: a board on which player places ships
    :type player_board: BattleshipBoard

    :param player_guess_board: a board where player will se his guesses
    :type player_guess_board: BattleshiBoard

    :param list_of_ships_lentgh: list of length of ships that will be placed
    :type list_of_ships_length: list
    """
    def __init__(self, board_size, list_of_ships_length):
        self._player_board = BattleshipBoard(board_size)
        self._player_guess_board = BattleshipBoard(board_size)
        self._list_of_ships_length = list_of_ships_length
        self._max_length = max(list_of_ships_length)

    def player_board(self):
        return self._player_board

    def player_guess_board(self):
        return self._player_guess_board

    def list_of_ships_length(self):
        return self._list_of_ships_length

    def guess(self, computer_board, position):
        """
        Allows to guess enemy ships and when whole ship found, sets squares around ship to attacked_sea
        """
        square = computer_board.get_square(position)
        if square == ship_ind:
            computer_board.set_square(position, attacked_ship_ind)
            self._player_guess_board.set_square(position, attacked_ship_ind)
            ship = computer_board.get_ship_if_whole_sunk(position, self._max_length)
            if ship:
                self._list_of_ships_length = remove_ship_length_from_list_of_lengths(ship.length(), self._list_of_ships_length)
                if self._list_of_ships_length:
                    self._max_length = max(self._list_of_ships_length)
                self._player_guess_board.set_squares_around_ship(ship, attacked_sea_ind)
                computer_board.set_squares_around_ship(ship, attacked_sea_ind)
        elif square == sea_ind:
            computer_board.set_square(position, attacked_sea_ind)
            self._player_guess_board.set_square(position, attacked_sea_ind)
            ship = computer_board.get_ship_if_whole_sunk(position, self._max_length)
            if ship:
                self._list_of_ships_length = remove_ship_length_from_list_of_lengths(ship.length(), self._list_of_ships_length)
                if self._list_of_ships_length:
                    self._max_length = max(self._list_of_ships_length)
                self._player_guess_board.set_squares_around_ship(ship, attacked_sea_ind)
                computer_board.set_squares_around_ship(ship, attacked_sea_ind)
        else:
            pass

    def place_ship(self, length):
        """
        Places ship in random position
        """
        while True:
            try:
                ship = generate_ship(length, self._player_board.size())
                self._player_board.place_ship(ship)
                return ship
            except CanNotPlaceShipError:
                pass
