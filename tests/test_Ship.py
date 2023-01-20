from game_files.ship import Ship
from game_files.ship import (
    IncorrectDirectionError,
    IncorrectLengthOfShipError,
    IncorrectPositionError,
    IncorrectSizeError,
    NoSuchCourseError
)
from game_files.defined_enumerations import Direction, Course
import pytest


def test_init():
    ship = Ship((1, 2), Direction.vertical, 1)
    assert ship.position() == (1, 2)
    assert ship.direction() == Direction.vertical
    assert ship.length() == 1


def test_init_wrong_position_1_dim():
    with pytest.raises(IncorrectPositionError):
        Ship((1), Direction.vertical, 4)


def test_init_wrong_position_more_than_2_dim():
    with pytest.raises(IncorrectPositionError):
        Ship((1, 2, 3), Direction.vertical, 4)


def test_init_wrong_direction():
    with pytest.raises(IncorrectDirectionError):
        Ship((1, 1), 'se', 2)


def test_init_wrong_length_negative():
    with pytest.raises(IncorrectLengthOfShipError):
        Ship((1, 1), Direction.vertical, -1)


def test_init_wrong_length_zero():
    with pytest.raises(IncorrectLengthOfShipError):
        Ship((1, 1), Direction.vertical, 0)


def test_fits_in_board_max_length():
    ship = Ship((0, 3), Direction.vertical, 5)
    assert ship.fits_in_board(5) is True


def test_fits_in_board_min_length():
    ship = Ship((0, 3), Direction.vertical, 1)
    assert ship.fits_in_board(5) is True


def test_fits_in_board_barely_out():
    ship = Ship((1, 3), Direction.vertical, 5)
    assert ship.fits_in_board(5) is False


def test_fits_in_board_out_by_a_lot():
    ship = Ship((3, 3), Direction.vertical, 10)
    assert ship.fits_in_board(5) is False


def test_fits_in_board_horizontal_small_length():
    ship = Ship((0, 3), Direction.horizontal, 2)
    assert ship.fits_in_board(5) is True


def test_fits_in_board_horizontal_min_length():
    ship = Ship((0, 3), Direction.horizontal, 1)
    assert ship.fits_in_board(5) is True


def test_fits_in_board_horizontal_barely_out():
    ship = Ship((1, 3), Direction.horizontal, 3)
    assert ship.fits_in_board(5) is False


def test_fits_in_board_horizontal_out_by_a_lot():
    ship = Ship((1, 3), Direction.horizontal, 10)
    assert ship.fits_in_board(5) is False


def test_fits_in_board_wrong_size():
    ship = Ship((0, 3), Direction.vertical, 5)
    with pytest.raises(IncorrectSizeError):
        ship.fits_in_board(-1)


def test_positions_typical():
    ship = Ship((0, 3), Direction.vertical, 3)
    assert ship.positions() == [(0, 3), (1, 3), (2, 3)]


def test_positions_one_square():
    ship = Ship((0, 3), Direction.vertical, 1)
    assert ship.positions() == [(0, 3)]


def test_positions_horizontal():
    ship = Ship((0, 3), Direction.horizontal, 3)
    assert ship.positions() == [(0, 3), (0, 4), (0, 5)]


def test_move_ship_north():
    ship = Ship((1, 3), Direction.vertical, 3)
    ship.move_ship(Course.north, 5)
    assert ship.position() == (0, 3)


def test_move_ship_west():
    ship = Ship((1, 3), Direction.vertical, 3)
    ship.move_ship(Course.west, 5)
    assert ship.position() == (1, 2)


def test_move_ship_south():
    ship = Ship((1, 3), Direction.vertical, 3)
    ship.move_ship(Course.south, 5)
    assert ship.position() == (2, 3)


def test_move_ship_east():
    ship = Ship((1, 3), Direction.vertical, 3)
    ship.move_ship(Course.east, 5)
    assert ship.position() == (1, 4)


def test_move_ship_no_space():
    ship = Ship((1, 3), Direction.vertical, 4)
    ship.move_ship(Course.south, 5)
    assert ship.position() == (1, 3)


def test_move_ship_wrong_course():
    ship = Ship((1, 3), Direction.vertical, 4)
    with pytest.raises(NoSuchCourseError):
        ship.move_ship('n', 5)


def test_rotate_vertical():
    ship = Ship((1, 2), Direction.vertical, 5)
    ship.rotate_ship(10)
    assert ship.direction() == Direction.horizontal


def test_rotate_horizontal():
    ship = Ship((1, 2), Direction.horizontal, 5)
    ship.rotate_ship(10)
    assert ship.direction() == Direction.vertical


def test_rotate_does_not_fit():
    ship = Ship((1, 2), Direction.vertical, 4)
    ship.rotate_ship(5)
    assert ship.direction() == Direction.vertical


def test_bool():
    ship = Ship((1, 2), Direction.vertical, 4)
    assert ship
