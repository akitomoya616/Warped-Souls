from AttackStrategy import AttackStrategy
from Player import Player
import random


class StrongAttack(AttackStrategy):

    def attack(self, player: Player):
        action_point_drained = 8
        chance_to_miss = 0.4

        if round(random.random(), 2) > chance_to_miss:
            damage_done = 10
        else:
            damage_done = 0
        return damage_done, action_point_drained
