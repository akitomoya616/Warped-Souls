import random

from MoveStrategy import MoveStrategy
import Helper


class HomingMovement(MoveStrategy):

    def homing_move_ai(self, player_loc: tuple, enemy_loc: tuple, enemy, board) -> list:

        """Takes the player and enemy location and provides a list of possible
        valid directions for homing movement."""

        player_x_loc, player_y_loc = player_loc
        enemy_x_loc, enemy_y_loc = enemy_loc

        homing_moves = []

        # Check if you have to move up or down.
        if player_x_loc > enemy_x_loc and ((Helper.get_next_coordinates('down', enemy_loc)) not in board.occupied_coords):
            homing_moves.append('down')
        elif player_x_loc < enemy_x_loc and ((Helper.get_next_coordinates('up', enemy_loc)) not in board.occupied_coords):
            homing_moves.append('up')
        else:
            pass

        # Check if you have to move left or right.
        if player_y_loc > enemy_y_loc and ((Helper.get_next_coordinates('right', enemy_loc)) not in board.occupied_coords):
            homing_moves.append('right')
        elif player_y_loc < enemy_y_loc and ((Helper.get_next_coordinates('left', enemy_loc)) not in board.occupied_coords):
            homing_moves.append('left')
        else:
            pass

        return homing_moves

    def homing_check(self, player_loc: tuple, enemy_loc: tuple):

        homing_moves = []

        player_x_loc, player_y_loc = player_loc
        enemy_x_loc, enemy_y_loc = enemy_loc

        if player_x_loc > enemy_x_loc:
            homing_moves.append('down')
        elif player_x_loc < enemy_x_loc:
            homing_moves.append('left')
        else:
            pass

        return homing_moves

    def barrier_check(self):
        pass

    def move(self, enemy, board):

        player = board.player
        player_loc = player.get_location()
        enemy_loc = enemy.get_location()

        homing_moves = self.homing_move_ai(player_loc, enemy_loc, enemy, board)

        # If we have moves that are valid
        if homing_moves:

            # Choose a random direction to move and delete the board's occupied cells info
            direction_chosen = random.choice(homing_moves)
            board.occupied_coords.remove((enemy.x_loc, enemy.y_loc))

            # Get the new coordinates and add new location to the board's occupied cells
            new_x_loc, new_y_loc = Helper.get_next_coordinates(direction_chosen, enemy_loc)
            board.occupied_coords.append((new_x_loc, new_y_loc))

            return new_x_loc, new_y_loc

        # If enemy is blocked from moving
        else:
            # Change enemy movement
            enemy.set_strategy("Random")
            enemy.action_points += 1
            return enemy_loc

