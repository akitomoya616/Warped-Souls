from AttackStrategy import AttackStrategy
import random


class NormalAttack(AttackStrategy):

    def attack(self, board):
        action_point_drained = 1
        chance_to_miss = 0.1

        player = board.player

        if round(random.random(), 2) > chance_to_miss:
            if player.hit_points >= 50:
                damage_done = 10
            elif player.hit_points >= 25:
                damage_done = 5
            else:
                damage_done = 3
        else:
            damage_done = 0
        return damage_done, action_point_drained
