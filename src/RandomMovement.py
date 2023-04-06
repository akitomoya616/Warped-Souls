import random

from MoveStrategy import MoveStrategy
import Helper


class RandomMovement(MoveStrategy):

    def move(self, enemy, board):

        enemy_loc = enemy.get_location()

        # Gets the possible random moves the enemy might do:
        feasible_cells = Helper.get_cardinal_coordinates(enemy_loc[0], enemy_loc[1],
                                                         board.num_rows, board.num_cols)

        print("Feasible Cells:")
        print(feasible_cells)

        feasible_cells = [cell for cell in feasible_cells if cell not in board.occupied_coords]

        # Set the enemy strategy back to homing
        enemy.set_strategy("Homing")

        if len(feasible_cells):
            board.occupied_coords.remove((enemy.x_loc, enemy.y_loc))
            new_x_loc, new_y_loc = random.choice(feasible_cells)
            board.occupied_coords.append((new_x_loc, new_y_loc))

            return new_x_loc, new_y_loc
        else:
            print("No place to move.")
