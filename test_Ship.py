from classes import Ship
from classes import (
    IncorrectDirectionError,
    IncorrectLengthOfShipError,
    IncorrectPositionError,
    IncorrectSizeError
)
import pytest


def test_init():
    ship = Ship((1, 2), 's', 1)
    assert ship.position() == (1, 2)
    assert ship.direction() == 's'
    assert ship.length() == 1


def test_init_wrong_position():
    with pytest.raises(IncorrectPositionError):
        Ship((1, 2, 3), 's', 4)
    with pytest.raises(IncorrectPositionError):
        Ship((1), 's', 4)


def test_init_wrong_direction():
    with pytest.raises(IncorrectDirectionError):
        Ship((1, 1), 'n', 2)
    with pytest.raises(IncorrectDirectionError):
        Ship((1, 1), 'se', 2)


def test_init_wrong_length():
    with pytest.raises(IncorrectLengthOfShipError):
        Ship((1, 1), 's', -1)
    with pytest.raises(IncorrectLengthOfShipError):
        Ship((1, 1), 's', 0)


def test_fits_in_board():
    ship = Ship((0, 3), 's', 5)
    assert ship.fits_in_board(5) is True
    ship = Ship((0, 3), 's', 1)
    assert ship.fits_in_board(5) is True
    ship = Ship((1, 3), 's', 5)
    assert ship.fits_in_board(5) is False
    ship = Ship((3, 3), 's', 10)
    assert ship.fits_in_board(5) is False
    ship = Ship((0, 3), 'e', 2)
    assert ship.fits_in_board(5) is True
    ship = Ship((0, 3), 'e', 1)
    assert ship.fits_in_board(5) is True
    ship = Ship((1, 3), 'e', 3)
    assert ship.fits_in_board(5) is False
    ship = Ship((1, 3), 'e', 10)
    assert ship.fits_in_board(5) is False


def test_fits_in_board_wrong_size():
    ship = Ship((0, 3), 's', 5)
    with pytest.raises(IncorrectSizeError):
        ship.fits_in_board(-1)


def test_positions():
    ship = Ship((0, 3), 's', 3)
    assert ship.positions() == [(0, 3), (1, 3), (2, 3)]
    ship = Ship((0, 3), 's', 1)
    assert ship.positions() == [(0, 3)]
    ship = Ship((0, 3), 'e', 3)
    assert ship.positions() == [(0, 3), (0, 4), (0, 5)]
