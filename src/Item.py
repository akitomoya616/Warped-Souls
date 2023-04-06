class Item:
    def __init__(self, x_loc, y_loc):
        self.x_loc = x_loc
        self.y_loc = y_loc

    def get_location(self):
        return self.x_loc, self.y_loc
