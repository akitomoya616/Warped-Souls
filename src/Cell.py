class Cell:
    def __init__(self, row, col, altitude, hidden_altitude, character):
        self.row = row
        self.col = col
        self.altitude = altitude
        self.hidden_altitude = hidden_altitude
        self.character = character  # 0: background, 1: player, 2: enemy type A, 3: enemy type B, 4: store
