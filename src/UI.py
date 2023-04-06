from datetime import datetime as datetime_, timedelta

from PySide6 import QtWidgets, QtGui, QtTest

import Constants
import Helper
from Shop import Shop
from Board import Board
from Inventory import Inventory
from Command import *
from CustomMessageBox import CustomMessageBox


class UI(QtWidgets.QWidget):

    def __init__(self):

        self.invShown = False  # bool that checks if the UI is currently displaying item list or not
        self.shopShown = False
        QtWidgets.QWidget.__init__(self)

        self.setWindowTitle('Warped Souls')

        self.setGeometry(0, 0, 2560, 1600)

        self.main_layout = QtWidgets.QHBoxLayout(self)

        # Create grid layout for map
        self.map = QtWidgets.QGridLayout()
        # self.inventory_widget = QtWidgets.QLabel()
        self.inventory_menu = QtWidgets.QGridLayout()
        self.shop_menu = QtWidgets.QGridLayout()

        # self.inventory_widget.addLayout(self.inventory_menu)

        # Create vertical layout to house info and commands
        self.info_commands = QtWidgets.QVBoxLayout()

        # Create vertical layout to put in information
        self.info = QtWidgets.QVBoxLayout()

        # Create three horizontal layouts: for buttons
        self.hl_one = QtWidgets.QHBoxLayout()
        self.hl_two = QtWidgets.QHBoxLayout()
        self.hl_three = QtWidgets.QHBoxLayout()

        # Horizontal Layout Level 1 Button(s)
        self.up_button = QtWidgets.QPushButton()
        self.hl_one.addWidget(self.up_button)
        self.up_button.setText("Up")

        # Horizontal Layout Level 2 Button(s)
        self.left_button = QtWidgets.QPushButton()
        self.left_button.setText("Left")
        self.down_button = QtWidgets.QPushButton()
        self.down_button.setText("Down")
        self.right_button = QtWidgets.QPushButton()
        self.right_button.setText("Right")

        # Set direction property to each direction button
        self.up_button.setProperty("direction", "up")
        self.down_button.setProperty("direction", "down")
        self.left_button.setProperty("direction", "left")
        self.right_button.setProperty("direction", "right")

        self.hl_two.addWidget(self.left_button)
        self.hl_two.addWidget(self.down_button)
        self.hl_two.addWidget(self.right_button)

        # Horizontal Layout Level 3 Button(s)
        self.inventory_button = QtWidgets.QPushButton()
        self.inventory_button.setText("Inventory")
        self.inventory_button.setProperty("inventory", "inventory")  # Assign inventory button with property "inventory"
        self.stats_button = QtWidgets.QPushButton()
        self.stats_button.setText("Statistics")
        self.stats_button.setProperty("stats", "stats")  # Assign stats button with property "stats"
        self.end_button = QtWidgets.QPushButton()
        self.end_button.setText("End Turn")
        self.end_button.setProperty("end_turn", "end turn")  # Assign end turn button with property "end_turn"

        self.hl_three.addWidget(self.inventory_button)
        self.hl_three.addWidget(self.stats_button)
        self.hl_three.addWidget(self.end_button)

        # Place information and Commands into 'info_commands' layout
        self.info_commands.addLayout(self.info)
        # self.info_commands.addLayout(self.inventory_menu)
        self.info_commands.addLayout(self.hl_one)
        self.info_commands.addLayout(self.hl_two)
        self.info_commands.addLayout(self.hl_three)

        # Place the map and the information inside the main_layout
        self.main_layout.addLayout(self.map)
        self.main_layout.addLayout(self.info_commands)

        self.msg = None

        self.is_player_turn = True

        # Define the total number of row and col that are going to use for building the map
        self.row_total = 12
        self.col_total = 12

        # Draw the grid
        self.board = Board(self.row_total, self.col_total)
        # The follow two lines can test if Singleton pattern has been applied correctly
        # self.board2 = Board(self.row_total, self.col_total)
        self.board_info = self.board.tile_info  # stores the 2d list for cell info

        self.inventory = Inventory(4, 4)
        self.inventory_info = self.inventory.get_inventory()

        self.shop = Shop()
        self.shop_info = self.shop.get_items()

        self.last_item_id_clicked = 0
        # list of lists that stores info for each button.
        # self.tile_info[a][b] = (row a, column b, button on row a, column b)
        # so self.tile_info[0][0][2] returns you the reference of the button at (0,0)
        self.tile_info = []
        self.inventory_slot_info = []
        self.shop_slot_info = []
        self.draw_map(self.board_info)

        self.spawn_player() # Generate on bottom left corner

        self.spawn_treasure() # Generate on any cell in the top row

        self.spawn_shop() # Generate on any cell, re-assign its coordinates if it is on an occupied cell

        # Health, Action and Magic Info
        self.health_label = QtWidgets.QLabel()
        self.action_label = QtWidgets.QLabel()
        self.magic_label = QtWidgets.QLabel()
        self.gold_label = QtWidgets.QLabel()
        self.info.addWidget(self.health_label)
        self.info.addWidget(self.action_label)
        self.info.addWidget(self.magic_label)
        self.info.addWidget(self.gold_label)

        self.spawn_enemy()

        # Connect the direction buttons with button_pressed method
        self.left_button.clicked.connect(self.button_pressed)
        self.right_button.clicked.connect(self.button_pressed)
        self.up_button.clicked.connect(self.button_pressed)
        self.down_button.clicked.connect(self.button_pressed)

        # Connect the item button
        self.inventory_button.clicked.connect(self.button_pressed)
        self.stats_button.clicked.connect(self.button_pressed)

        # Connect the end turn button
        self.end_button.clicked.connect(self.button_pressed)

        self.update_info()

    @staticmethod
    def q_wait(t):
        end = datetime_.now() + timedelta(milliseconds=t)
        while datetime_.now() < end:
            QtGui.QGuiApplication.processEvents()

    QtTest.QTest.qWait = q_wait

    def update_info(self):

        # Update Health Value
        health_value = self.board.player.hit_points
        self.health_label.setText("HP: " + str(health_value))

        # Update Action Value
        action_value = self.board.player.action_points
        self.action_label.setText("AP: " + str(action_value))

        # Update Magic Value
        magic_value = self.board.player.magic_points
        self.magic_label.setText("MP: " + str(magic_value))

        gold_value = self.board.player.gold
        self.gold_label.setText("Gold: " + str(gold_value))

    # Generate the map with 12 x 12 clickable buttons assigned with different altitude property.
    # Assign pixmap to them with corresponding altitude data.
    def draw_map(self, board_info):

        for row_list in board_info:

            buttons_in_row = []

            for cell in row_list:
                loc = QtWidgets.QPushButton(self)  # try to make it like squares but not rectangle buttons
                # reassign each button's width and height to 50 to make it a square but not a rectangle
                loc.setFixedHeight(50)
                loc.setFixedWidth(50)

                # Assign the cell with the current button
                loc.setProperty("cell", cell)

                # Get necessary properties from the cell and assign them to the button.
                row = cell.row
                loc.setProperty("row", row)  # Create a property in loc named "row", and assign row value to it

                column = cell.col
                loc.setProperty("column", column)

                altitude = cell.altitude
                loc.setProperty("altitude", altitude)

                hidden_altitude = cell.hidden_altitude
                loc.setProperty("hidden_altitude", hidden_altitude)

                loc.setProperty("character", 0)

                pixmap = QtGui.QPixmap(Constants.altitude_image_dictionary[str(altitude)])
                Helper.assign_texture(pixmap, loc)

                # Append loc to buttons_in_row
                buttons_in_row.append((row, column, loc))

                # Assign methods for each icon on the map after it was clicked
                loc.clicked.connect(self.button_pressed)

                self.map.addWidget(loc, row, column)

            # Append entire row information to tile_info
            self.tile_info.append(buttons_in_row)

    def spawn_player(self):

        # (BACKEND) Create a Player and add it to the board
        self.board.spawn_player()

        initial_player_x_loc = self.board.player.x_loc
        initial_player_y_loc = self.board.player.y_loc

        button_at_loc = self.tile_info[initial_player_x_loc][initial_player_y_loc][2]
        background_image_path = Constants.altitude_image_dictionary[str(button_at_loc.property("altitude"))]
        foreground_image_path = Constants.character_image_dictionary[self.board.player.character]
        button_after_pixmap = Helper.image_merge(background_image_path, foreground_image_path)

        button_at_loc.setProperty("character", self.board.player.character)

        Helper.assign_texture(button_after_pixmap, button_at_loc)

    def spawn_treasure(self):
        self.board.spawn_treasure()

        initial_treasure_x_loc = self.board.treasure.x_loc
        initial_treasure_y_loc = self.board.treasure.y_loc

        button_at_loc = self.tile_info[initial_treasure_x_loc][initial_treasure_y_loc][2]
        background_image_path = Constants.altitude_image_dictionary[str(button_at_loc.property("altitude"))]
        foreground_image_path = Constants.general_image_dictionary["4_treasure"]
        button_after_pixmap = Helper.image_merge(background_image_path, foreground_image_path)

        Helper.assign_texture(button_after_pixmap, button_at_loc)

    def spawn_shop(self):
        self.board.spawn_shop()

        initial_shop_x_loc = self.board.shop.x_loc
        initial_shop_y_loc = self.board.shop.y_loc

        button_at_loc = self.tile_info[initial_shop_x_loc][initial_shop_y_loc][2]
        background_image_path = Constants.altitude_image_dictionary[str(button_at_loc.property("altitude"))]
        foreground_image_path = "../images/Shop.png"
        button_after_pixmap = Helper.image_merge(background_image_path, foreground_image_path)

        Helper.assign_texture(button_after_pixmap, button_at_loc)

    def spawn_enemy(self):

        self.board.trigger_enemies()

        for enemy in self.board.enemies:

            x_loc = enemy.x_loc
            y_loc = enemy.y_loc

            button_at_enemy_loc = self.tile_info[x_loc][y_loc][2]
            background_image_path = Constants.altitude_image_dictionary[str(button_at_enemy_loc.property("altitude"))]
            foreground_image_path = Constants.character_image_dictionary[enemy.character]
            button_after_pixmap = Helper.image_merge(background_image_path, foreground_image_path)

            button_at_enemy_loc.setProperty("character", enemy.character)

            Helper.assign_texture(button_after_pixmap, button_at_enemy_loc)

    def despawn_character(self, row, column):

        button_at_loc = self.tile_info[row][column][2]

        altitude_of_loc = button_at_loc.property("altitude")
        button_background = QtGui.QPixmap(Constants.altitude_image_dictionary[str(altitude_of_loc)])
        Helper.assign_texture(button_background, button_at_loc)

        button_at_loc.setProperty("character", 0)

        # (BACKEND) Remove it from occupied co-ordinates
        self.board.occupied_coords.remove((row, column))

    def draw_inventory(self, tile_info):

        for row_list in tile_info:

            buttons_in_row = []

            for item_cell in row_list:

                loc = QtWidgets.QPushButton(self)  # try to make it like squares but not rectangle buttons
                # reassign each button's width and height to 50 to make it a square but not a rectangle
                loc.setFixedHeight(50)
                loc.setFixedWidth(50)

                # Assign the cell with the current button
                loc.setProperty("item_cell", item_cell)

                # Get necessary properties from the cell and assign them to the button.
                row = item_cell.row
                loc.setProperty("row", row)  # Create a property in loc named "row", and assign row value to it

                column = item_cell.col
                loc.setProperty("column", column)

                item_id = item_cell.get_item_id()
                loc.setProperty("item_id", item_id)

                # Assign pixmap to the button with corresponding altitude value
                if item_id == 1:
                    pixmap = QtGui.QPixmap("../images/Potion.jpg")
                elif item_id == 2:
                    pixmap = QtGui.QPixmap("../images/ChocolateBar.jpg")
                elif item_id == 3:
                    pixmap = QtGui.QPixmap("../images/Fireball.jpg") 
                else:  
                    pixmap = QtGui.QPixmap("../images/Null.jpg")

                Helper.assign_texture(pixmap, loc)

                # Append loc to buttons_in_row
                buttons_in_row.append((row, column, loc))

                # Assign methods for each icon on the map after it was clicked
                loc.clicked.connect(self.button_pressed)

                self.inventory_menu.addWidget(loc, row, column)

            # Append entire row information to tile_info
            self.inventory_slot_info.append(buttons_in_row)

    def draw_shop(self, tile_info):

        for row_list in tile_info:

            buttons_in_row = []

            for shop_cell in row_list:

                loc = QtWidgets.QPushButton(self)  # try to make it like squares but not rectangle buttons
                # reassign each button's width and height to 50 to make it a square but not a rectangle
                loc.setFixedHeight(50)
                loc.setFixedWidth(50)

                # Assign the cell with the current button
                loc.setProperty("shop_cell", shop_cell)

                # Get necessary properties from the cell and assign them to the button.
                row = shop_cell.row
                loc.setProperty("row", row)  # Create a property in loc named "row", and assign row value to it

                column = shop_cell.col
                loc.setProperty("column", column)

                item_id = shop_cell.get_item_id()
                loc.setProperty("item_id", item_id)

                # Assign pixmap to the button with corresponding altitude value
                if item_id == 1:
                    pixmap = QtGui.QPixmap("../images/Potion.jpg")
                elif item_id == 2:
                    pixmap = QtGui.QPixmap("../images/ChocolateBar.jpg")
                elif item_id == 3:
                    pixmap = QtGui.QPixmap("../images/Fireball.jpg") 
                else:  
                    pixmap = QtGui.QPixmap("../images/Null.jpg")

                Helper.assign_texture(pixmap, loc)

                # Append loc to buttons_in_row
                buttons_in_row.append((row, column, loc))

                # Assign methods for each icon on the map after it was clicked
                loc.clicked.connect(self.button_pressed)

                self.shop_menu.addWidget(loc, row, column)

            # Append entire row information to tile_info
            self.shop_slot_info.append(buttons_in_row)

    def new_turn(self):

        self.is_player_turn = True  # Set player's turn to true

        # Set up the player with fresh action points
        self.board.player.refresh_action_points()
        for enemy in self.board.enemies:
            enemy.refresh_action_points()

        # Enable movement and inventory buttons
        self.toggle_movement_buttons(True)
        self.toggle_inventory_button(True)
        self.end_button.setEnabled(True)

        # Update the info
        self.update_info()

    def show_enemy_turn(self):
        for index, enemy in enumerate(self.board.enemies):
            # Type is 0 if it's an Attack and 1 if it's Movement
            # Details returns players health after the attack or
            # new location if it's movement
            player = self.board.player
            while enemy.action_points > 0 and player.hit_points > 0:

                action_type, details = enemy.action(self.board)
                self.q_wait(500)

                if action_type == 1:

                    self.tile_info[enemy.x_loc][enemy.y_loc][2].setProperty("character", 0)
                    before_button = self.tile_info[enemy.x_loc][enemy.y_loc][2]
                    after_button = self.tile_info[details[0]][details[1]][2]

                    before_button.setProperty("character", 0)
                    after_button.setProperty("character", enemy.character)

                    self.move_character(enemy.character, before_button, after_button)

                    # (BACKEND) Update the enemy location
                    enemy.x_loc = details[0]
                    enemy.y_loc = details[1]
                else:
                    # (BACKEND) Decrease player hit points
                    player.hit_points = player.hit_points - details

                    self.update_info()

    def toggle_movement_buttons(self, toggle_value: bool):
        self.up_button.setEnabled(toggle_value)
        self.down_button.setEnabled(toggle_value)
        self.left_button.setEnabled(toggle_value)
        self.right_button.setEnabled(toggle_value)

    def toggle_inventory_button(self, toggle_value: bool):
        self.inventory_button.setEnabled(toggle_value)

    # Method for handling a character's movement from one cell to another
    def move_character(self, character, button_before, button_after):

        self.hidden_altitude_check(character, button_after)

        # Update Before Cell #

        # Get altitude of the before cell
        altitude_before = button_before.property("altitude")

        # Get pixmap based on altitude
        button_before_pixmap = QtGui.QPixmap(Constants.altitude_image_dictionary[str(altitude_before)])

        # Update Before Texture
        Helper.assign_texture(button_before_pixmap, button_before)

        # Update After Cell #

        # Get altitude of the after cell
        altitude_after = button_after.property("altitude")

        # Generate the pixmap based on altitude and character
        background_image_path = Constants.altitude_image_dictionary[str(altitude_after)]
        foreground_image_path = Constants.character_image_dictionary[character]
        button_after_pixmap = Helper.image_merge(background_image_path, foreground_image_path)

        # Update After Texture
        Helper.assign_texture(button_after_pixmap, button_after)

    def show_message_box(self, window_title, window_text):

        self.msg = QMessageBox()
        self.msg.setWindowTitle(window_title)
        self.msg.setText(window_text)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec()

    # Change the altitude to hidden altitude once the player moves to a new cell
    def hidden_altitude_check(self, character, button_after):
        if character == 1:  # If this move was made by the player
            altitude = button_after.property("altitude")
            hidden_altitude = button_after.property("hidden_altitude")
            if altitude != hidden_altitude:
                altitude_difference = altitude - hidden_altitude
                button_after.setProperty("altitude", hidden_altitude)

                # Process fall damage
                player = self.board.player
                hp_lost = 5 * altitude_difference
                player.hit_points = player.hit_points - hp_lost

                # Show a pop-up message box on UI and close it automatically after 2 seconds
                message = "before: " + str(altitude) + ", after: " + str(
                    button_after.property("altitude")) + ". You lost " + str(hp_lost) + " hp."
                CustomMessageBox.showWithTimeout(1, message, "Terrain Collapsed!", QMessageBox.Warning)

                if player.hit_points <= 0:
                    self.show_message_box("Game Over", "You Died!")
                    self.toggle_movement_buttons(False)
                    self.toggle_inventory_button(False)
                    self.end_button.setEnabled(False)



    def button_pressed(self):  # COMMAND PATTERN applied here
        obj = self.sender()  # Get the reference of the button that has been clicked
        command_controller = CommandController()  # Set up controller for handling commands

        # Get the property of the button
        property_byte = obj.dynamicPropertyNames()  # Get all property names set to this button in byte code
        property_str = bytes(property_byte[0]).decode()  # Get the first property name, and decode it into string

        command = NullCommand()
        # Run corresponding command based on the button's property
        if property_str == "direction":
            command = DirectionCommand(self)
        elif property_str == "inventory":
            command = InventoryCommand(self)
        elif property_str == "end_turn":
            command = EndTurnCommand(self)
        elif property_str == "cell":
            command = MapCommand(self)
        elif property_str == "item_cell":
            command = ItemCommand(self)
        elif property_str == "shop_cell":
            command = ShopItemCommand(self)
        elif property_str == "stats":
            command = StatsCommand(self)
        command_controller.set_command(command)
        command_controller.execute()
