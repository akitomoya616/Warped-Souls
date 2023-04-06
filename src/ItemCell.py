class ItemCell:
    def __init__(self, row, col, item_id):
        self.row = row
        self.col = col
        self.item_id = item_id

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def set_item_id(self, item_id):
        self.item_id = item_id

    def get_item_id(self):
        return self.item_id



