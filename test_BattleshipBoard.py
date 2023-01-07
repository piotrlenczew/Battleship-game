from classes import BattleshipBoard, Ship
from classes import remove_ship_length_from_list_of_lengths
from classes import (
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
    player_board = BattleshipBoard(10, [['X'] * 10 for row in range(10)])
    board = player_board.board()
    for row in board:
        for square in row:
            assert square == 'X'


def test_init_more_or_less_rows():
    with pytest.raises(WrongAmountOfRowsError):
        BattleshipBoard(9, [['X'] * 10 for row in range(10)])
    with pytest.raises(WrongAmountOfRowsError):
        BattleshipBoard(10, [['X'] * 10 for row in range(11)])
    with pytest.raises(WrongAmountOfRowsError):
        BattleshipBoard(5, [['X'] * 4 for row in range(4)])
    with pytest.raises(WrongAmountOfRowsError):
        BattleshipBoard(5, [['X'] * 5 for row in range(4)])


def test_init_more_elements_in_rows():
    with pytest.raises(WrongAmountOfSquaresInRowsError):
        BattleshipBoard(10, [['X'] * 11 for row in range(10)])


def test_init_wrong_indication():
    with pytest.raises(WrongIndicationOfSquare):
        BattleshipBoard(10, [['Y'] * 10 for row in range(10)])


def test_init_three_element_string():
    with pytest.raises(MoreThanOneSymbolInSquareError):
        BattleshipBoard(10, [['XYZ'] * 10 for row in range(10)])


def test_init_board_not_given():
    player_board = BattleshipBoard(10)
    board = player_board.board()
    for row in board:
        for square in row:
            assert square == ' '


def test_init_0_or_negative_size():
    with pytest.raises(IncorrectSizeError):
        BattleshipBoard(0)
    with pytest.raises(IncorrectSizeError):
        BattleshipBoard(-2)
    with pytest.raises(IncorrectSizeError):
        BattleshipBoard(0, [['X'] * 1 for row in range(1)])


# def test_set_board():
#     player_board = BattleshipBoard(5)
#     player_board.set_board(10, [['X'] * 10 for row in range(10)])
#     board = player_board.board()
#     assert len(board) == 10
#     for row in board:
#         for square in row:
#             assert square == 'X'


# def test_Board_set_board_more_rows():
#     player_board = BattleshipBoard()
#     with pytest.raises(WrongAmountOfRowsError):
#         player_board.set_board([['X'] * 10 for row in range(11)])


# def test_Board_set_board_more_elements_in_rows():
#     player_board = BattleshipBoard()
#     with pytest.raises(WrongAmountOfSquaresInRowsError):
#         player_board.set_board([['X'] * 11 for row in range(10)])


# def test_Board_set_board_wrong_indication():
#     player_board = BattleshipBoard()
#     with pytest.raises(WrongIndicationOfSquare):
#         player_board.set_board([['Y'] * 10 for row in range(10)])


# def test_Board_set_board_three_element_string():
#     player_board = BattleshipBoard()
#     with pytest.raises(MoreThanOneSymbolInSquareError):
#         player_board.set_board([['XYZ'] * 10 for row in range(10)])


def test_get_square():
    player_board = BattleshipBoard(3)
    assert player_board.get_square((1, 2)) == ' '


def test_get_square_out_of_range():
    player_board = BattleshipBoard(10)
    with pytest.raises(PositionOutOfBoardError):
        player_board.get_square((1, 10))


def test_set_square():
    player_board = BattleshipBoard(5)
    player_board.set_square((1, 4), '~')
    assert player_board.get_square((1, 4)) == '~'
    player_board.set_square((2, 4), 'X')
    assert player_board.get_square((2, 4)) == 'X'
    player_board.set_square((0, 4), 'O')
    assert player_board.get_square((0, 4)) == 'O'


def test_set_square_wrong_position():
    player_board = BattleshipBoard(10)
    with pytest.raises(PositionOutOfBoardError):
        player_board.set_square((10, 4), '~')


def test_set_square_wrong_amount_of_symbols():
    player_board = BattleshipBoard(5)
    with pytest.raises(MoreThanOneSymbolInSquareError):
        player_board.set_square((1, 4), '~ ')


def test_set_square_wrong_symbol():
    player_board = BattleshipBoard(5)
    with pytest.raises(WrongIndicationOfSquare):
        player_board.set_square((1, 4), 'F')


def test_has_ship_false():
    player_board = BattleshipBoard(9)
    assert not player_board.has_ship()
    player_board.set_square((8, 3), 'X')
    assert not player_board.has_ship()


def test_has_ship_true():
    player_board = BattleshipBoard(9)
    player_board.set_square((2, 4), 'O')
    assert player_board.has_ship()


def test_ship_near():
    player_board = BattleshipBoard(10)
    assert not player_board.ship_near((5, 6))


def test_ship_near_on_edge():
    player_board = BattleshipBoard(10)
    assert not player_board.ship_near((9, 9))


def test_ship_near_can_not_place():
    player_board = BattleshipBoard(10)
    player_board.set_square((6, 6), 'O')
    assert player_board.ship_near((5, 6))
    player_board.set_square((6, 6), ' ')
    assert not player_board.ship_near((5, 6))
    player_board.set_square((6, 5), 'X')
    assert player_board.ship_near((5, 6))


def test_ship_near_is_range_good():
    player_board = BattleshipBoard(10)
    player_board.set_square((3, 4), 'X')
    assert not player_board.ship_near((1, 2))


def test_can_place_ship():
    ship = Ship((1, 2), 's', 3)
    player_board = BattleshipBoard(4)
    assert player_board.can_place_ship(ship)


def test_can_place_ship_too_small_board():
    ship = Ship((1, 2), 's', 5)
    player_board = BattleshipBoard(4)
    player_board.set_square((0, 0), 'O')
    assert not player_board.can_place_ship(ship)


def test_can_place_ship_on_another_ship():
    ship = Ship((1, 2), 's', 3)
    player_board = BattleshipBoard(4)
    player_board.set_square((1, 2), 'O')
    assert not player_board.can_place_ship(ship)


def test_can_place_ship_interferes_with_another_ship():
    ship = Ship((1, 2), 's', 3)
    player_board = BattleshipBoard(4)
    player_board.set_square((1, 1), 'O')
    assert not player_board.can_place_ship(ship)


def test_place_ship():
    ship1 = Ship((1, 2), 's', 3)
    player_board = BattleshipBoard(7)
    player_board.place_ship(ship1)
    for number in range(1, 4):
        assert player_board.board()[number][2] == 'O'
    ships = 0
    sea_squares = 0
    for row in player_board.board():
        for square in row:
            if square == ' ':
                sea_squares += 1
            elif square == 'O':
                ships += 1
    assert sea_squares == 46
    assert ships == 3
    ship2 = Ship((0, 4), 'e', 3)
    player_board.place_ship(ship2)
    for number in range(4, 7):
        assert player_board.board()[0][number] == 'O'
    ships = 0
    sea_squares = 0
    for row in player_board.board():
        for square in row:
            if square == ' ':
                sea_squares += 1
            elif square == 'O':
                ships += 1
    assert sea_squares == 43
    assert ships == 6


def test_place_ship_too_small_board():
    ship1 = Ship((1, 2), 's', 3)
    player_board = BattleshipBoard(3)
    with pytest.raises(CanNotPlaceShipError):
        player_board.place_ship(ship1)


def test_place_ship_interferes_with_other_ship():
    ship1 = Ship((1, 2), 's', 3)
    player_board = BattleshipBoard(7)
    player_board.place_ship(ship1)
    ship2 = Ship((4, 3), 'e', 3)
    with pytest.raises(CanNotPlaceShipError):
        player_board.place_ship(ship2)


def test_squares_around_ship():
    player_board = BattleshipBoard(10)
    ship = Ship((0, 0), 's', 5)
    player_board.place_ship(ship)
    player_board.set_squares_around_ship(ship, '~')
    number_of_att_sea = 0
    number_of_ship_squares = 0
    for row in player_board.board():
        for square in row:
            if square == 'O':
                number_of_ship_squares += 1
            if square == '~':
                number_of_att_sea += 1
    assert number_of_ship_squares == 5
    assert number_of_att_sea == 7


def test_remove_ship_length_from_list_of_legths():
    list_of_ships_length = [2,5]
    ship_length = 5
    list_of_ships_length = remove_ship_length_from_list_of_lengths(ship_length, list_of_ships_length)
    assert list_of_ships_length == [2]
    ship_length = 2
    list_of_ships_length = remove_ship_length_from_list_of_lengths(ship_length, list_of_ships_length)
    assert list_of_ships_length == []