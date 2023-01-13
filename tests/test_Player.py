from battleship_game.ship import Ship
from battleship_game.player import Player
from battleship_game.computer_player import ComputerPlayer
from battleship_game.square_indications import sea_ind, ship_ind, attacked_sea_ind, attacked_ship_ind


def test_place_ship():
    pass


def test_place_ship_over_board():
    pass


def test_place_ship_on_other_ship():
    pass


def test_guess(monkeypatch):
    computer_player = ComputerPlayer(10, [2, 4])
    ship = Ship((2, 4), 'v', 2)

    def not_random_ship(length, board_size):
        return ship
    monkeypatch.setattr('players.generate_ship', not_random_ship)
    computer_player.place_ship(2)

    player = Player(10, [2, 4])
    player.guess(computer_player.computer_board(), (0, 0))
    assert player.player_guess_board().get_square((0, 0)) == attacked_sea_ind
    assert player.player_guess_board().get_square((0, 1)) == sea_ind
    assert computer_player.computer_board().get_square((0, 0)) == attacked_sea_ind
    assert computer_player.computer_board().get_square((0, 1)) == sea_ind
    player.guess(computer_player.computer_board(), (2, 4))
    assert player.player_guess_board().get_square((2, 4)) == attacked_ship_ind
    assert player.player_guess_board().get_square((3, 4)) == sea_ind
    assert computer_player.computer_board().get_square((2, 4)) == attacked_ship_ind
    assert computer_player.computer_board().get_square((3, 4)) == ship_ind
    player.guess(computer_player.computer_board(), (3, 4))
    player.guess(computer_player.computer_board(), (4, 4))
    player.guess(computer_player.computer_board(), (1, 4))
    assert player._player_guess_board.get_square((3, 3)) == attacked_sea_ind
    assert player.list_of_ships_length() == [4]


def test_Player_guess_diffrent_board_sizes():
    pass
