from classes import Ship, BattleshipBoard, Player, ComputerPlayer
from classes import generate_position
from classes import CanNotPlaceShipError
import pytest


def test_Player_place_ship():
    player = Player(10)
    ship = Ship((0, 0), 'e', 2)
    player.place_ship(ship)
    assert player.player_board().get_square((0, 0)) == 'O'
    assert player.player_board().get_square((0, 1)) == 'O'
    assert player.player_board().get_square((1, 0)) == ' '
    assert player.player_board().get_square((1, 1)) == ' '


def test_Player_place_ship_over_board():
    player = Player(10)
    ship = Ship((0, 0), 'e', 11)
    with pytest.raises(CanNotPlaceShipError):
        player.place_ship(ship)


def test_Player_place_ship_on_other_ship():
    player = Player(10)
    ship1 = Ship((1, 0), 'e', 3)
    player.place_ship(ship1)
    with pytest.raises(CanNotPlaceShipError):
        ship2 = Ship((0, 0), 's', 3)
        player.place_ship(ship2)


def test_ComputerPlayer_place_ship(monkeypatch):
    computer_player = ComputerPlayer(10, [4])
    ship = Ship((1, 2), 's', 4)

    def not_random_ship(length, board_size):
        return ship
    monkeypatch.setattr('classes.generate_ship', not_random_ship)
    computer_player.place_ship(4)
    assert computer_player.computer_board().get_square((1, 2)) == 'O'
    assert computer_player.computer_board().get_square((2, 2)) == 'O'
    assert computer_player.computer_board().get_square((3, 2)) == 'O'
    assert computer_player.computer_board().get_square((4, 2)) == 'O'
    assert computer_player.computer_board().get_square((5, 2)) == ' '
    assert computer_player.computer_board().get_square((1, 3)) == ' '


def test_Player_guess(monkeypatch):
    computer_player = ComputerPlayer(10, [5])
    ship = Ship((2, 4), 's', 5)

    def not_random_ship(length, board_size):
        return ship
    monkeypatch.setattr('classes.generate_ship', not_random_ship)
    computer_player.place_ship(5)

    player = Player(10)
    player.guess(computer_player.computer_board(), (0, 0))
    assert player.player_guess_board().get_square((0, 0)) == '~'
    assert player.player_guess_board().get_square((0, 1)) == ' '
    assert computer_player.computer_board().get_square((0, 0)) == '~'
    assert computer_player.computer_board().get_square((0, 1)) == ' '
    player.guess(computer_player.computer_board(), (2, 4))
    assert player.player_guess_board().get_square((2, 4)) == 'X'
    assert player.player_guess_board().get_square((3, 4)) == ' '
    assert computer_player.computer_board().get_square((2, 4)) == 'X'
    assert computer_player.computer_board().get_square((3, 4)) == 'O'


def test_Player_guess_diffrent_board_sizes():
    pass


# def test_ComputerPlayer_guess():
#     player = Player(10)
#     ship = Ship((2, 5), 'e', 5)
#     player.place_ship(ship)

#     computer_player = ComputerPlayer(10)
#     pass


# def test_ComputerPlayer_guess_diffrent_board_sizes():
#     pass


def test_generate_position():
    position = generate_position(10)
    row, column = position
    assert row < 10 and row >= 0
