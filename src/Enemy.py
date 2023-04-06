from Character import Character
from MoveStrategy import MoveStrategy
from AttackStrategy import AttackStrategy
from StrongAttack import StrongAttack
from HomingMovement import HomingMovement
from RandomMovement import RandomMovement
import Helper


class Enemy(Character):

    def __init__(self, max_hit_points, max_magic_points, max_action_points,
                 hit_points, magic_points, action_points,
                 x_loc, y_loc, move_strategy: MoveStrategy,
                 attack_strategy: AttackStrategy):

        super().__init__(max_hit_points, max_magic_points, max_action_points,
                         hit_points, magic_points, action_points, x_loc, y_loc)

        self.max_hit_points = max_hit_points
        self.max_magic_points = max_magic_points
        self.max_action_points = max_action_points

        self.hit_points = hit_points
        self.magic_points = magic_points
        self.action_points = action_points

        self.x_loc = x_loc
        self.y_loc = y_loc

        self.move_strategy = move_strategy
        self.attack_strategy = attack_strategy
        self.character = None

        self.gold = None

    def check_player_attackable(self, board):
        player_loc = (board.player.x_loc, board.player.y_loc)

        board_rows = board.num_rows
        board_cols = board.num_cols

        if player_loc in Helper.get_adjacent_coordinates(self.x_loc, self.y_loc, board_rows, board_cols):
            player_attackable = True
        else:
            player_attackable = False

        return player_attackable

    def action(self, board):
        if self.check_player_attackable(board):
            damage_done, drained_ap = self.attack(board)
            self.action_points -= drained_ap
            return 0, damage_done
        else:
            self.action_points -= 1
            new_x_loc, new_y_loc = self.move(board)
            return 1, (new_x_loc, new_y_loc)

    def move(self, board):
        return self.move_strategy.move(self, board)

    def attack(self, board):
        return self.attack_strategy.attack(board)

    def reduce_health(self, hit_points):
        self.hit_points -= hit_points
        if self.hit_points <= (self.max_hit_points // 2):
            self.attack_strategy = StrongAttack()

    def set_strategy(self, move_type: str):
        if move_type == "Homing":
            self.move_strategy = HomingMovement()
            print("Strategy was set to homing.")
        elif move_type == "Random":
            self.move_strategy = RandomMovement()
        else:
            self.move_strategy = RandomMovement()
