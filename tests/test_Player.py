from game_files.ship import Ship
from game_files.battleshipboard import BattleshipBoard
from game_files.player import Player
from game_files.game_settings import (
    sea_ind, ship_ind, attacked_sea_ind, attacked_ship_ind
)
from game_files.defined_enumerations import Direction


def test_place_ship():
    player = Player(10, [2, 3, 4])
    player.place_ship(3)
    ship_squares = 0
    for row in player.player_board().board():
        for square in row:
            if square == ship_ind:
                ship_squares += 1
    assert ship_squares == 3


def test_guess_one_ship_guessed():
    enemy_board = BattleshipBoard(10)
    ship = Ship((2, 4), Direction.vertical, 2)
    enemy_board.place_ship(ship)

    player = Player(10, [2, 4])
    player.guess(enemy_board, (0, 0))
    assert player.player_guess_board().get_square((0, 0)) == attacked_sea_ind
    assert player.player_guess_board().get_square((0, 1)) == sea_ind
    assert enemy_board.get_square((0, 0)) == attacked_sea_ind
    assert enemy_board.get_square((0, 1)) == sea_ind
    player.guess(enemy_board, (2, 4))
    assert player.player_guess_board().get_square((2, 4)) == attacked_ship_ind
    assert player.player_guess_board().get_square((3, 4)) == sea_ind
    assert enemy_board.get_square((2, 4)) == attacked_ship_ind
    assert enemy_board.get_square((3, 4)) == ship_ind
    player.guess(enemy_board, (3, 4))
    player.guess(enemy_board, (4, 4))
    player.guess(enemy_board, (1, 4))
    assert player._player_guess_board.get_square((3, 3)) == attacked_sea_ind
    assert player.list_of_ships_length() == [4]


def test_guess_one_ship_guessed_near_border():
    enemy_board = BattleshipBoard(10)
    ship = Ship((0, 0), Direction.vertical, 3)
    enemy_board.place_ship(ship)

    player = Player(10, [3, 4])
    player.guess(enemy_board, (9, 9))
    assert player.player_guess_board().get_square((9, 9)) == attacked_sea_ind
    assert player.player_guess_board().get_square((9, 8)) == sea_ind
    assert enemy_board.get_square((9, 9)) == attacked_sea_ind
    assert enemy_board.get_square((9, 8)) == sea_ind
    player.guess(enemy_board, (0, 0))
    assert player.player_guess_board().get_square((0, 0)) == attacked_ship_ind
    assert player.player_guess_board().get_square((0, 1)) == sea_ind
    assert enemy_board.get_square((0, 0)) == attacked_ship_ind
    assert enemy_board.get_square((0, 1)) == sea_ind
    player.guess(enemy_board, (1, 0))
    player.guess(enemy_board, (2, 0))
    player.guess(enemy_board, (3, 0))
    assert player._player_guess_board.get_square((2, 1)) == attacked_sea_ind
    assert player.list_of_ships_length() == [4]


def test_guess_one_ship_guessed_sea_before():
    enemy_board = BattleshipBoard(10)
    ship = Ship((1, 1), Direction.vertical, 3)
    enemy_board.place_ship(ship)

    player = Player(10, [3, 4])
    player.guess(enemy_board, (0, 1))
    assert player.player_guess_board().get_square((0, 1)) == attacked_sea_ind
    assert player.player_guess_board().get_square((0, 0)) == sea_ind
    assert enemy_board.get_square((0, 1)) == attacked_sea_ind
    assert enemy_board.get_square((0, 0)) == sea_ind
    player.guess(enemy_board, (1, 1))
    assert player.player_guess_board().get_square((1, 1)) == attacked_ship_ind
    assert player.player_guess_board().get_square((1, 2)) == sea_ind
    assert enemy_board.get_square((1, 1)) == attacked_ship_ind
    assert enemy_board.get_square((1, 2)) == sea_ind
    player.guess(enemy_board, (2, 1))
    player.guess(enemy_board, (3, 1))
    player.guess(enemy_board, (4, 1))
    assert player._player_guess_board.get_square((4, 2)) == attacked_sea_ind
    assert player.list_of_ships_length() == [4]
