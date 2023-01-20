from game_files.computer_player import ComputerPlayer
from game_files.game_settings import (
    ship_ind, attacked_sea_ind, attacked_ship_ind
)
from game_files.defined_enumerations import Direction
from game_files.ship import Ship
from game_files.battleshipboard import BattleshipBoard


def test_place_ship():
    computer_player = ComputerPlayer(10, [2, 3, 4])
    computer_player.place_ship(3)
    ship_squares = 0
    for row in computer_player.computer_board().board():
        for square in row:
            if square == ship_ind:
                ship_squares += 1
    assert ship_squares == 3


def test_guess_one_ship(monkeypatch):
    player_board = BattleshipBoard(10)
    computer_player = ComputerPlayer(10, [2, 4])
    ship = Ship((2, 4), Direction.vertical, 2)

    player_board.place_ship(ship)

    def not_random_position(board_size):
        return (2, 4)
    monkeypatch.setattr('game_files.computer_player.generate_position', not_random_position)
    computer_player.guess(player_board)
    assert player_board.get_square((2, 4)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((1, 4)) == attacked_sea_ind

    computer_player.guess(player_board)
    assert player_board.get_square((2, 3)) == attacked_sea_ind

    computer_player.guess(player_board)
    assert player_board.get_square((3, 4)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((4, 4)) == attacked_sea_ind

    assert player_board.get_square((2, 5)) == attacked_sea_ind
    assert computer_player.list_of_ships_length() == [4]


def test_guess_one_ship_near_border(monkeypatch):
    player_board = BattleshipBoard(10)
    computer_player = ComputerPlayer(10, [3, 4])
    ship = Ship((0, 0), Direction.vertical, 3)

    player_board.place_ship(ship)

    def not_random_position(board_size):
        return (1, 0)
    monkeypatch.setattr('game_files.computer_player.generate_position', not_random_position)
    computer_player.guess(player_board)
    assert player_board.get_square((1, 0)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((0, 0)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((2, 0)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((3, 0)) == attacked_sea_ind

    assert player_board.get_square((3, 1)) == attacked_sea_ind
    assert computer_player.list_of_ships_length() == [4]


def test_guess_one_ship_guessed_sea_before(monkeypatch):
    player_board = BattleshipBoard(10)
    computer_player = ComputerPlayer(10, [3, 4])
    ship = Ship((0, 0), Direction.vertical, 3)

    player_board.place_ship(ship)

    def not_random_position(board_size):
        return (3, 0)
    monkeypatch.setattr('game_files.computer_player.generate_position', not_random_position)
    computer_player.guess(player_board)
    assert player_board.get_square((3, 0)) == attacked_sea_ind

    def not_random_position(board_size):
        return (1, 0)
    monkeypatch.setattr('game_files.computer_player.generate_position', not_random_position)
    computer_player.guess(player_board)
    assert player_board.get_square((1, 0)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((0, 0)) == attacked_ship_ind

    computer_player.guess(player_board)
    assert player_board.get_square((2, 0)) == attacked_ship_ind

    def not_random_position(board_size):
        return (9, 9)
    monkeypatch.setattr('game_files.computer_player.generate_position', not_random_position)
    computer_player.guess(player_board)
    assert player_board.get_square((9, 9)) == attacked_sea_ind

    assert player_board.get_square((3, 1)) == attacked_sea_ind
    assert computer_player.list_of_ships_length() == [4]
