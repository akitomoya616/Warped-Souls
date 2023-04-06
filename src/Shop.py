from ItemCell import ItemCell
from PySide6.QtWidgets import QMessageBox


class Shop:

    def __init__(self):

        # Get a reference to the player

        # list of lists that stores info for each cell.
        # self.tile_info[a][b] = (reference of the cell on row a, column b)
        self.tile_info = []

        self.grid_size = 12

        # Define the total number of row and col that are going to use for building the map
        self.num_rows = 1
        self.num_cols = 3

        self.row_pointer = 0
        self.col_pointer = 0

        # Draw the grid
        self.create_inventory()

    # Generate the map with 12 x 12 clickable buttons assigned with different altitude property.
    # Assign pixmap to them with corresponding altitude data.
    def create_inventory(self):

        for row in range(self.num_rows):

            row_info = []

            for column in range(self.num_cols):
                cell = ItemCell(row, column, 0)
                row_info.append(cell)

            # Append entire row information to tile_info
            self.tile_info.append(row_info)
            self.tile_info[0][0].set_item_id(1)
            self.tile_info[0][1].set_item_id(2)
            self.tile_info[0][2].set_item_id(3)

    def get_items(self):
        return self.tile_info

    def get_num_rows(self):
        return self.num_rows

    def get_num_cols(self):
        return self.num_cols

    def add_to_inventory(self, UI, item_id):
        spotFound = False
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if (spotFound == False):
                    if (self.tile_info[i][j].get_item_id() == 0):
                        self.tile_info[i][j].set_item_id(item_id)
                        spotFound = True

        if not spotFound:
            UI.msg = QMessageBox()
            UI.msg.setWindowTitle("Inventory Full!")
            UI.msg.setText('There is no room for this item in your inventory!')
            UI.msg.setIcon(QMessageBox.Warning)
            UI.msg.exec()
