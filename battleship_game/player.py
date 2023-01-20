from game_files.defined_enumerations import Direction
from game_files.ship import Ship
from game_files.battleshipboard import BattleshipBoard, CanNotPlaceShipError
from random import randint
from game_files.game_settings import (
    sea_ind, ship_ind, attacked_sea_ind, attacked_ship_ind
)


def generate_position(board_size):
    """Generate random position in board of given size."""
    row = randint(0, board_size - 1)
    column = randint(0, board_size - 1)
    return (row, column)


def generate_ship(length, board_size):
    """Generate ship of given length that fits in board of given size."""
    position = generate_position(board_size)
    condition = randint(0, 1)
    if condition == 0:
        direction = Direction.vertical
    else:
        direction = Direction.horizontal
    ship = Ship(position, direction, length)
    return ship


def remove_ship_length_from_list_of_lengths(ship_length, list_of_ships_length):
    """Return a list that contains elements of list_of_ships_length axcept given ship_length."""
    result = []
    found_one = False
    for length in list_of_ships_length:
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
        """Initalize instance of Player."""
        self._player_board = BattleshipBoard(board_size)
        self._player_guess_board = BattleshipBoard(board_size)
        self._list_of_ships_length = list_of_ships_length
        self._max_length = max(list_of_ships_length)

    def player_board(self):
        """Get player_board attribute."""
        return self._player_board

    def player_guess_board(self):
        """Get player_guess_board attribute"""
        return self._player_guess_board

    def list_of_ships_length(self):
        """Get list_of_ships_length attribute"""
        return self._list_of_ships_length

    def guess(self, computer_board, position):
        """
        Guess square in given position and akt accordinly.

        - When sea_ind found, change square to attacked_ship_ind
        - When ship_ind found, change square to attacked_ship_ind
        - If whole ship was found change squares around ship to attacked_sea_ind
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
        """Place ship in random position."""
        while True:
            try:
                ship = generate_ship(length, self._player_board.size())
                self._player_board.place_ship(ship)
                return ship
            except CanNotPlaceShipError:
                pass
