from Character import Character
import Helper


class Player(Character):
    def __init__(self, max_hit_points, max_magic_points, max_action_points,
                 hit_points, magic_points, action_points,
                 y_loc, x_loc):
        super().__init__(max_hit_points, max_magic_points, max_action_points,
                         hit_points, magic_points, action_points,
                         y_loc, x_loc)

        self.inventory = None

        self.max_hit_points = max_hit_points
        self.max_magic_points = max_magic_points
        self.max_action_points = max_action_points
        self.hit_points = hit_points
        self.magic_points = magic_points
        self.action_points = action_points
        self.gold = 0
        self.y_loc = y_loc
        self.x_loc = x_loc

        self.character = 1

        self.movable = True
        self.observers = []

    def reduce_action_points(self, ap):
        self.action_points -= ap

    def move_player(self, direction):
        # Reduce Action Points for Movement
        self.reduce_action_points(1)

        # Get the new coordinates after Movement in a particular Direction
        new_x_loc, new_y_loc = Helper.get_next_coordinates(direction, self.get_location())
        self.set_location((new_x_loc, new_y_loc))
        return new_x_loc, new_y_loc

    def set_location(self, location):
        self.x_loc, self.y_loc = location

    def get_inventory(self):
        return self.inventory

    def add_gold(self, gold_found):
        self.gold += gold_found
