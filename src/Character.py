from Subject import Subject


class Character(Subject):

    def __init__(self, max_hit_points, max_magic_points, max_action_points,
                 hit_points, magic_points, action_points,
                 x_loc, y_loc):
        self.max_hit_points = max_hit_points
        self.max_magic_points = max_magic_points
        self.max_action_points = max_action_points

        self.hit_points = hit_points
        self.magic_points = magic_points
        self.action_points = action_points
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.observers = []

    def refresh_action_points(self):
        self.action_points = self.max_action_points

    def get_location(self):
        return self.x_loc, self.y_loc

    def registerObserver(self, o):
        self.observers.append(o)

    def removeObserver(self, o):
        self.observers.remove(o)

    def notifyObservers(self, message, value):
        for o in self.observers:
            o.update(message, value)
