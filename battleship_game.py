from classes import Ship, Player, ComputerPlayer
from from_square_name_to_position import from_square_name_to_position


def enter_ship(length):
    square_name = input('Podaj nazwę pola: ')
    position = from_square_name_to_position[square_name.upper()]
    direction = input('Podaj kierunek statku [s/e]: ')
    ship = Ship(position, direction, length)
    return ship


computer = ComputerPlayer(10, [2, 3, 3, 4, 5])
computer.place_ship(2)
computer.place_ship(3)
computer.place_ship(3)
computer.place_ship(4)
computer.place_ship(5)

player = Player(10)
print("Rozpoczynamy grę!\nNa początku ustaw statki.")
Destroyer = enter_ship(2)
player.place_ship(Destroyer)
print(str(player.player_board()))
Submarine = enter_ship(3)
player.place_ship(Submarine)
print(str(player.player_board()))
Cruiser = enter_ship(3)
player.place_ship(Cruiser)
print(str(player.player_board()))
Battleship = enter_ship(4)
player.place_ship(Battleship)
print(str(player.player_board()))
Carrier = enter_ship(5)
player.place_ship(Carrier)
print(str(player.player_board()))

while player.player_board().has_ship() and computer.computer_board().has_ship():
    square_name = input('Podaj nazwę pola w które strzelasz: ')
    attacked_position = from_square_name_to_position[square_name.upper()]
    player.guess(computer.computer_board(), attacked_position)
    print(str(player.player_guess_board()))
    print('\n')
    if not computer.computer_board().has_ship():
        print('Gratulacje wygrałeś!')
    else:
        computer.guess(player.player_board())
        print(str(player.player_board()))
        if not player.player_board().has_ship():
            print('Niestety przegrałeś')
