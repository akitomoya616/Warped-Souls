from Enemy import Enemy
from MoveStrategy import MoveStrategy
from AttackStrategy import AttackStrategy


class Zombie(Enemy):

    def __init__(self, max_hit_points, max_magic_points, max_action_points,
                 hit_points, magic_points, action_points,
                 x_loc, y_loc, move_strategy: MoveStrategy,
                 attack_strategy: AttackStrategy):

        super().__init__(max_hit_points, max_magic_points, max_action_points,
                         hit_points, magic_points, action_points, x_loc, y_loc,
                         move_strategy, attack_strategy)

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

        self.character = 4

        self.gold = 35
