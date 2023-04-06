import random

import Enemy
from Goblin import Goblin
from Vampire import Vampire
from Skeleton import Skeleton
from Zombie import Zombie
from HomingMovement import HomingMovement
from NormalAttack import NormalAttack
from RandomMovement import RandomMovement
from StrongAttack import StrongAttack


class EnemyFactory:

    def __init__(self):
        self.enemy = None

    def create_enemy(self, enemy_type: int, board) -> Enemy:

        # Create an enemy on the board
        x_loc = random.randint(0, board.num_cols - 1)
        y_loc = random.randint(0, board.num_rows - 1)

        flag = 1
        while flag:
            if (x_loc, y_loc) not in board.occupied_coords:
                board.occupied_coords.append((x_loc, y_loc))
                flag = 0
            else:
                x_loc = random.randint(0, board.num_cols - 1)
                y_loc = random.randint(0, board.num_rows - 1)

        if enemy_type == 2:
            self.enemy = Goblin(150, 10, 8, 150, 10, 8, x_loc, y_loc, HomingMovement(), NormalAttack())

        elif enemy_type == 3:
            self.enemy = Vampire(150, 10, 8, 150, 10, 8, x_loc, y_loc, HomingMovement(), NormalAttack())

        elif enemy_type == 4:
            self.enemy = Zombie(150, 10, 8, 150, 10, 8, x_loc, y_loc, HomingMovement(), NormalAttack())

        elif enemy_type == 5:
            self.enemy = Skeleton(150, 10, 8, 150, 10, 8, x_loc, y_loc, HomingMovement(), NormalAttack())

        return self.enemy
