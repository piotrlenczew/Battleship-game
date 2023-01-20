from game_files.game_settings import (
    sea_ind,
    attacked_sea_ind,
    ship_ind,
    attacked_ship_ind
)
from game_files.defined_enumerations import Direction
from game_files.ship import Ship
from game_files.battleshipboard import BattleshipBoard
from game_files.battleshipboard import (
    IncorrectSizeError,
    WrongIndicationOfSquare,
    WrongAmountOfSquaresInRowsError,
    WrongAmountOfRowsError,
    MoreThanOneSymbolInSquareError,
    PositionOutOfBoardError,
    CanNotPlaceShipError
)
import pytest


def test_init():
    player_board = BattleshipBoard(10, [[attacked_ship_ind] * 10 for row in range(10)])
    board = player_board.board()
    assert len(board) == 10
    for row in board:
        assert len(row) == 10
        for square in row:
            assert square == attacked_ship_ind


def test_init_more_rows():
    with pytest.raises(WrongAmountOfRowsError):
        BattleshipBoard(9, [[ship_ind] * 10 for row in range(10)])


def test_init_less_rows():
    with pytest.raises(WrongAmountOfRowsError):
        BattleshipBoard(5, [[ship_ind] * 4 for row in range(4)])


def test_init_more_elements_in_rows():
    with pytest.raises(WrongAmountOfSquaresInRowsError):
        BattleshipBoard(10, [[ship_ind] * 11 for row in range(10)])


def test_init_wrong_indication():
    with pytest.raises(WrongIndicationOfSquare):
        BattleshipBoard(10, [['Y'] * 10 for row in range(10)])


def test_init_three_element_string():
    with pytest.raises(MoreThanOneSymbolInSquareError):
        BattleshipBoard(10, [['XYZ'] * 10 for row in range(10)])


def test_init_board_not_given():
    player_board = BattleshipBoard(10)
    board = player_board.board()
    assert len(board) == 10
    for row in board:
        assert len(row) == 10
        for square in row:
            assert square == sea_ind


def test_init_0_or_negative_size():
    with pytest.raises(IncorrectSizeError):
        BattleshipBoard(0)
    with pytest.raises(IncorrectSizeError):
        BattleshipBoard(-2)
    with pytest.raises(IncorrectSizeError):
        BattleshipBoard(0, [[ship_ind] * 1 for row in range(1)])


def test_get_square():
    player_board = BattleshipBoard(3)
    assert player_board.get_square((1, 2)) == sea_ind


def test_get_square_out_of_range():
    player_board = BattleshipBoard(10)
    with pytest.raises(PositionOutOfBoardError):
        player_board.get_square((1, 10))


def test_set_square():
    player_board = BattleshipBoard(5)
    player_board.set_square((1, 4), attacked_sea_ind)
    assert player_board.get_square((1, 4)) == attacked_sea_ind
    player_board.set_square((2, 4), attacked_ship_ind)
    assert player_board.get_square((2, 4)) == attacked_ship_ind
    player_board.set_square((0, 4), ship_ind)
    assert player_board.get_square((0, 4)) == ship_ind


def test_set_square_wrong_position():
    player_board = BattleshipBoard(10)
    with pytest.raises(PositionOutOfBoardError):
        player_board.set_square((10, 4), sea_ind)


def test_set_square_wrong_amount_of_symbols():
    player_board = BattleshipBoard(5)
    with pytest.raises(MoreThanOneSymbolInSquareError):
        player_board.set_square((1, 4), '~ ')


def test_set_square_wrong_symbol():
    player_board = BattleshipBoard(5)
    with pytest.raises(WrongIndicationOfSquare):
        player_board.set_square((1, 4), 'F')


def test_position_in_board():
    player_board = BattleshipBoard(5)
    assert not player_board.position_in_board((-1, -1))
    assert not player_board.position_in_board((-1, 3))
    assert not player_board.position_in_board((5, 5))
    assert player_board.position_in_board((4, 4))


def test_has_ship_false():
    player_board = BattleshipBoard(9)
    assert not player_board.has_ship()
    player_board.set_square((8, 3), attacked_ship_ind)
    assert not player_board.has_ship()


def test_has_ship_true():
    player_board = BattleshipBoard(9)
    player_board.set_square((2, 4), ship_ind)
    assert player_board.has_ship()


def test_ship_near():
    player_board = BattleshipBoard(10)
    assert not player_board.ship_near((5, 6))


def test_ship_near_on_edge():
    player_board = BattleshipBoard(10)
    assert not player_board.ship_near((9, 9))
    ship = Ship((9, 0), Direction.horizontal, 5)
    player_board.place_ship(ship)
    assert not player_board.ship_near((0, 0))
    assert not player_board.ship_near((9, 9))


def test_ship_near_can_not_place():
    player_board = BattleshipBoard(10)
    player_board.set_square((6, 6), ship_ind)
    assert player_board.ship_near((5, 6))
    player_board.set_square((6, 6), sea_ind)
    assert not player_board.ship_near((5, 6))
    player_board.set_square((6, 5), attacked_ship_ind)
    assert player_board.ship_near((5, 6))


def test_ship_near_is_range_good():
    player_board = BattleshipBoard(10)
    player_board.set_square((3, 4), attacked_ship_ind)
    assert not player_board.ship_near((1, 2))


def test_can_place_ship():
    ship = Ship((1, 2), Direction.vertical, 3)
    player_board = BattleshipBoard(4)
    assert player_board.can_place_ship(ship)


def test_can_place_ship_too_small_board():
    ship = Ship((1, 2), Direction.vertical, 5)
    player_board = BattleshipBoard(4)
    player_board.set_square((0, 0), ship_ind)
    assert not player_board.can_place_ship(ship)


def test_can_place_ship_on_another_ship():
    ship = Ship((1, 2), Direction.vertical, 3)
    player_board = BattleshipBoard(4)
    player_board.set_square((1, 2), ship_ind)
    assert not player_board.can_place_ship(ship)


def test_can_place_ship_interferes_with_another_ship():
    ship = Ship((1, 2), Direction.vertical, 3)
    player_board = BattleshipBoard(4)
    player_board.set_square((1, 1), ship_ind)
    assert not player_board.can_place_ship(ship)


def test_place_ship():
    ship1 = Ship((1, 2), Direction.vertical, 3)
    player_board = BattleshipBoard(7)
    player_board.place_ship(ship1)
    for number in range(1, 4):
        assert player_board.board()[number][2] == ship_ind
    ships = 0
    sea_squares = 0
    for row in player_board.board():
        for square in row:
            if square == sea_ind:
                sea_squares += 1
            elif square == ship_ind:
                ships += 1
    assert sea_squares == 46
    assert ships == 3
    ship2 = Ship((0, 4), Direction.horizontal, 3)
    player_board.place_ship(ship2)
    for number in range(4, 7):
        assert player_board.board()[0][number] == ship_ind
    ships = 0
    sea_squares = 0
    for row in player_board.board():
        for square in row:
            if square == sea_ind:
                sea_squares += 1
            elif square == ship_ind:
                ships += 1
    assert sea_squares == 43
    assert ships == 6


def test_place_ship_too_small_board():
    ship1 = Ship((1, 2), Direction.vertical, 3)
    player_board = BattleshipBoard(3)
    with pytest.raises(CanNotPlaceShipError):
        player_board.place_ship(ship1)


def test_place_ship_interferes_with_other_ship():
    ship1 = Ship((1, 2), Direction.vertical, 3)
    player_board = BattleshipBoard(7)
    player_board.place_ship(ship1)
    ship2 = Ship((4, 3), Direction.horizontal, 3)
    with pytest.raises(CanNotPlaceShipError):
        player_board.place_ship(ship2)


def test_set_squares_around_ship_s():
    player_board = BattleshipBoard(10)
    ship = Ship((0, 0), Direction.vertical, 5)
    player_board.place_ship(ship)
    player_board.set_squares_around_ship(ship, attacked_sea_ind)
    number_of_att_sea = 0
    number_of_ship_squares = 0
    for row in player_board.board():
        for square in row:
            if square == ship_ind:
                number_of_ship_squares += 1
            if square == attacked_sea_ind:
                number_of_att_sea += 1
    assert number_of_ship_squares == 5
    assert number_of_att_sea == 7
    assert player_board.get_square((5, 0)) == attacked_sea_ind
    assert player_board.get_square((5, 1)) == attacked_sea_ind
    assert player_board.get_square((4, 1)) == attacked_sea_ind
    assert player_board.get_square((3, 1)) == attacked_sea_ind
    assert player_board.get_square((2, 1)) == attacked_sea_ind
    assert player_board.get_square((1, 1)) == attacked_sea_ind
    assert player_board.get_square((0, 1)) == attacked_sea_ind


def test_set_squares_around_ship_e():
    player_board = BattleshipBoard(10)
    ship = Ship((0, 0), Direction.horizontal, 5)
    player_board.place_ship(ship)
    player_board.set_squares_around_ship(ship, attacked_sea_ind)
    number_of_att_sea = 0
    number_of_ship_squares = 0
    for row in player_board.board():
        for square in row:
            if square == ship_ind:
                number_of_ship_squares += 1
            if square == attacked_sea_ind:
                number_of_att_sea += 1
    assert number_of_ship_squares == 5
    assert number_of_att_sea == 7
    assert player_board.get_square((0, 5)) == attacked_sea_ind
    assert player_board.get_square((1, 5)) == attacked_sea_ind
    assert player_board.get_square((1, 4)) == attacked_sea_ind
    assert player_board.get_square((1, 3)) == attacked_sea_ind
    assert player_board.get_square((1, 2)) == attacked_sea_ind
    assert player_board.get_square((1, 1)) == attacked_sea_ind
    assert player_board.get_square((1, 0)) == attacked_sea_ind


def test_set_squares_around_ship_one_square():
    player_board = BattleshipBoard(10)
    ship = Ship((0, 0), Direction.horizontal, 1)
    player_board.place_ship(ship)
    player_board.set_squares_around_ship(ship, attacked_sea_ind)
    number_of_att_sea = 0
    number_of_ship_squares = 0
    for row in player_board.board():
        for square in row:
            if square == ship_ind:
                number_of_ship_squares += 1
            if square == attacked_sea_ind:
                number_of_att_sea += 1
    assert number_of_ship_squares == 1
    assert number_of_att_sea == 3
    assert player_board.get_square((0, 1)) == attacked_sea_ind
    assert player_board.get_square((1, 1)) == attacked_sea_ind
    assert player_board.get_square((1, 0)) == attacked_sea_ind


def test_remove_ship():
    player_board = BattleshipBoard(10)
    ship = Ship((0, 0), Direction.horizontal, 5)
    player_board.place_ship(ship)
    assert player_board.get_square((0, 0)) == ship_ind
    assert player_board.get_square((0, 4)) == ship_ind
    player_board.remove_ship(ship)
    assert player_board.get_square((0, 0)) == sea_ind
    assert player_board.get_square((4, 0)) == sea_ind


def test_get_ship_if_whole_sunk():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 1), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    player_board.set_square((2, 5), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 3), 5)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.horizontal
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_from_sea():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 1), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    player_board.set_square((2, 5), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 5), 5)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.horizontal
    assert ship1.length() == 3
    player_board.set_square((4, 2), attacked_sea_ind)
    player_board.set_square((4, 3), attacked_ship_ind)
    player_board.set_square((4, 4), attacked_ship_ind)
    player_board.set_square((4, 5), attacked_sea_ind)
    ship2 = player_board.get_ship_if_whole_sunk((4, 5), 5)
    assert ship2.position() == (4, 3)
    assert ship2.direction() == Direction.horizontal
    assert ship2.length() == 2


def test_get_ship_if_whole_sunk_from_sea_max_length_change():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 1), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 4), 3)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.horizontal
    assert ship1.length() == 3
    player_board.set_square((4, 2), attacked_sea_ind)
    player_board.set_square((4, 3), attacked_ship_ind)
    player_board.set_square((4, 4), attacked_ship_ind)
    ship2 = player_board.get_ship_if_whole_sunk((4, 4), 2)
    assert ship2.position() == (4, 3)
    assert ship2.direction() == Direction.horizontal
    assert ship2.length() == 2


def test_get_ship_if_whole_sunk_near_border():
    player_board = BattleshipBoard(10)
    player_board.set_square((0, 0), attacked_ship_ind)
    player_board.set_square((1, 0), attacked_ship_ind)
    player_board.set_square((2, 0), attacked_ship_ind)
    player_board.set_square((3, 0), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 0), 5)
    assert ship1.position() == (0, 0)
    assert ship1.direction() == Direction.vertical
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_near_border_south():
    player_board = BattleshipBoard(10)
    player_board.set_square((7, 1), attacked_ship_ind)
    player_board.set_square((8, 1), attacked_ship_ind)
    player_board.set_square((9, 1), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((7, 1), 3)
    assert ship1.position() == (7, 1)
    assert ship1.direction() == Direction.vertical
    assert ship1.length() == 3


def test_get_ship_if_whole_one_square_ship():
    player_board = BattleshipBoard(10)
    player_board.set_square((1, 0), attacked_sea_ind)
    player_board.set_square((2, 0), attacked_ship_ind)
    player_board.set_square((3, 0), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 0), 5)
    assert not ship1


def test_get_ship_if_whole_one_square_ship_border():
    player_board = BattleshipBoard(10)
    player_board.set_square((0, 0), attacked_ship_ind)
    player_board.set_square((1, 0), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((0, 0), 5)
    assert not ship1
    ship1 = player_board.get_ship_if_whole_sunk((1, 0), 5)
    assert not ship1
    player_board.set_square((0, 1), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((1, 0), 5)
    assert ship1


def test_get_ship_if_whole_sunk_max_length():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 1), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 3), 3)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.horizontal
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_but_not_know():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 5), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    player_board.set_square((2, 5), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 3), 5)
    assert not ship1


def test_get_ship_if_whole_sunk_from_att_sea_max_length():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 1), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 1), 3)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.horizontal
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_att_sea_but_wrong_ship():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 1), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((2, 3), attacked_ship_ind)
    player_board.set_square((2, 4), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((2, 1), 3)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.horizontal
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_v():
    player_board = BattleshipBoard(10)
    player_board.set_square((1, 2), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((3, 2), attacked_ship_ind)
    player_board.set_square((4, 2), attacked_ship_ind)
    player_board.set_square((5, 2), attacked_sea_ind)
    ship1 = player_board.get_ship_if_whole_sunk((4, 2), 5)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.vertical
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_max_length_v():
    player_board = BattleshipBoard(10)
    player_board.set_square((1, 2), attacked_sea_ind)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((3, 2), attacked_ship_ind)
    player_board.set_square((4, 2), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((4, 2), 3)
    assert ship1.position() == (2, 2)
    assert ship1.direction() == Direction.vertical
    assert ship1.length() == 3


def test_get_ship_if_whole_sunk_but_not_know_v():
    player_board = BattleshipBoard(10)
    player_board.set_square((2, 2), attacked_ship_ind)
    player_board.set_square((3, 2), attacked_ship_ind)
    player_board.set_square((4, 2), attacked_ship_ind)
    ship1 = player_board.get_ship_if_whole_sunk((4, 2), 5)
    assert not ship1
