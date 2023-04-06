import random
from Cell import Cell
from Player import Player
from EnemyFactory import EnemyFactory
import Constants
import Helper
from Observer import StatTracker


# Singleton code was copied (and partially edited by our own) from:
# https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
from Item import Item


def singleton(cls):
    _instance = {}

    def inner(num_rows, num_cols):
        if cls not in _instance:
            _instance[cls] = cls(num_rows, num_cols)
        return _instance[cls]

    return inner


@singleton
class Board:

    def __init__(self, num_rows, num_cols):

        # Get reference to all the enemies
        self.enemies = []

        self.player = None

        # list of lists that stores info for each cell.
        # self.tile_info[a][b] = (reference of the cell on row a, column b)
        self.tile_info = []

        self.grid_size = 12

        # Define the total number of row and col that are going to use for building the map
        self.num_rows = num_rows
        self.num_cols = num_cols

        # Draw the grid
        self.create_map()

        # Contains all the cells that are inhabited by characters (X Location, Y Location)
        self.occupied_coords = []
        self.stat_tracker = StatTracker() #OBSERVER PATTERN

    # Generate the map with 12 x 12 clickable buttons assigned with different altitude property.
    # Assign pixmap to them with corresponding altitude data.
    def create_map(self):

        for row in range(self.num_rows):

            row_info = []

            for column in range(self.num_cols):
                # Assign altitude property into the button within range [0, 5].
                if column == 0:  # If first cell in a row, randomly assign its altitude
                    altitude = random.randint(0, 3)
                else:  # Otherwise, assign its altitude based on the last cell's altitude
                    altitude_difference = random.randint(-2, 2)
                    altitude = row_info[column - 1].altitude - altitude_difference
                    # Make sure the altitude is still in [0, 3]
                    if altitude < 0:
                        altitude = 0
                    elif altitude > 3:
                        altitude = 3
                # 10% of chance for a cell to have hidden altitude different from altitude (1 - 3 unit(s) lower)
                chance = random.randint(0, 9)
                if chance == 0:
                    altitude_difference = random.randint(1, 3)
                    lower_altitude = altitude - altitude_difference
                    if lower_altitude < 0:
                        lower_altitude = 0
                    hidden_altitude = lower_altitude
                else:
                    hidden_altitude = altitude

                # Generate a cell object based on the given info
                # And append that cell to row_info
                cell = Cell(row, column, altitude, hidden_altitude, 0)
                row_info.append(cell)

            # Append entire row information to tile_info
            self.tile_info.append(row_info)

    def check_player_movable(self, direction):
        # Checks board edge constraints
        if direction == 'left':
            if self.player.y_loc == 0 or Helper.get_next_coordinates(direction,
                                                                     self.player.get_location()) in self.occupied_coords:
                return False
        elif direction == 'right':
            if self.player.y_loc == self.num_cols - 1 or Helper.get_next_coordinates(direction,
                                                                                     self.player.get_location()) in self.occupied_coords:
                return False
        elif direction == 'up':
            if self.player.x_loc == 0 or Helper.get_next_coordinates(direction,
                                                                     self.player.get_location()) in self.occupied_coords:
                return False
        elif direction == 'down':
            if self.player.x_loc == self.num_rows - 1 or Helper.get_next_coordinates(direction,
                                                                                     self.player.get_location()) in self.occupied_coords:
                return False

        return True

    def player_reach_treasure(self, direction):
        # Return true if player reaches the treasure box
        if Helper.get_next_coordinates(direction, self.player.get_location()) == (self.treasure.x_loc, self.treasure.y_loc):
            return True
        else:
            return False

    def spawn_player(self):
        self.player = Player(100, 50, 10, 100, 50, 10, 0, 11)
        self.player.registerObserver(self.stat_tracker)
        self.occupied_coords.append((self.player.get_location()))

    def spawn_enemy(self):
        enemy = EnemyFactory().create_enemy(random.choice(Constants.enemy_types), self)
        return enemy

    def spawn_treasure(self):
        self.treasure = Item(0, random.randint(0, self.num_rows - 1))
        self.occupied_coords.append((self.treasure.get_location()))
        return self.treasure

    def spawn_shop(self):
        # Generate the row and col for the shop
        (row, col) = random.randint(0, self.num_cols - 1), random.randint(0, self.num_rows - 1)
        # Re-generate the row and col for the shop until it can be placed on that location
        while (row, col) in self.occupied_coords:
            (row, col) = (random.randint(0, self.num_cols - 1), random.randint(0, self.num_rows - 1))
        # Generate the shop using this set of coordinates
        self.shop = Item(row, col)
        self.occupied_coords.append((self.shop.get_location()))
        return self.shop

    def trigger_enemies(self):

        for i in range(5):
            enemy = self.spawn_enemy()
            self.enemies.append(enemy)
