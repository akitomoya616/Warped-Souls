import random
from abc import ABC, abstractmethod
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMessageBox

import Helper

# all methods needed for Command Pattern have been implemented here

class Command(ABC):

    @abstractmethod
    def process(self):
        """An abstract command interface method for concrete commands to implement."""


class CommandController:
    """Invoker class that sets and calls commands."""

    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def execute(self):
        self.command.process()


class DirectionCommand:
    def __init__(self, ui):
        self.ui = ui

    def process(self):
        # Get the current direction button that had just been clicked
        ui = self.ui
        direction_button_clicked = ui.sender()

        # Get player reference
        player = ui.board.player

        # Check which direction the button is pointing to
        direction = direction_button_clicked.property("direction")

        # Check if player successfully reached the treasure box
        if ui.board.player_reach_treasure(direction):
            # Get coordinate for player and the treasure
            current_x_loc = player.x_loc
            current_y_loc = player.y_loc
            future_x_loc, future_y_loc = player.move_player(direction)
            # Run the move_character method to move the player to the treasure box cell
            ui.move_character(1, ui.tile_info[current_x_loc][current_y_loc][2],
                              ui.tile_info[future_x_loc][future_y_loc][2])

            # (UI) Updates Health, Action Points and Magic Points for the Player
            ui.update_info()

            ui.show_message_box("Congratulations", "You Win!")

            # Disable all buttons for player to interact with
            ui.toggle_movement_buttons(False)
            ui.toggle_inventory_button(False)
            ui.end_button.setEnabled(False)

            ui.is_player_turn = False  # Set the player's turn to false

        else:

            # Check if the player can be moved
            if ui.board.check_player_movable(direction):

                # Get player's current row and col value
                current_x_loc = player.x_loc
                current_y_loc = player.y_loc

                ui.tile_info[current_x_loc][current_y_loc][2].setProperty("character", 0)
                ui.board.occupied_coords.remove((current_x_loc, current_y_loc))

                # (BACKEND) Calls for an update to the player location
                future_x_loc, future_y_loc = player.move_player(direction)

                ui.tile_info[future_x_loc][future_y_loc][2].setProperty("character", 1)
                ui.board.occupied_coords.append((future_x_loc, future_y_loc))

                ui.move_character(1, ui.tile_info[current_x_loc][current_y_loc][2],
                                  ui.tile_info[future_x_loc][future_y_loc][2])
                player.notifyObservers("Distance Travelled", 1)
                # (ui) Updates Health, Action Points and Magic Points for the Player
                ui.update_info()
                if player.action_points <= 0:
                    ui.toggle_movement_buttons(False)
                    ui.toggle_inventory_button(False)
            else:
                message = f"Cannot move {direction}."
                ui.show_message_box("Invalid Move", message)


class InventoryCommand:
    def __init__(self, ui):
        self.ui = ui

    def process(self):
        ui = self.ui
        if ui.shopShown:
            ui.msg = QMessageBox()
            ui.msg.setWindowTitle("System Message")
            ui.msg.setText('You can not open your inventory until you leave the shop.')
            ui.msg.setIcon(QMessageBox.Warning)
            ui.msg.exec()
        elif ui.invShown:
            # show board
            for row in ui.inventory_slot_info:
                for loc_tuple in row:
                    loc_tuple[2].setIconSize(QSize(0, 0))
                    ui.inventory_menu.removeWidget(loc_tuple[2])
                    loc_tuple[2].close()
            ui.info_commands.removeItem(ui.inventory_menu)
            # self.inventory_menu.hide()
            ui.invShown = False

            # Enable all direction buttons and End Turn button
            ui.toggle_movement_buttons(True)
            ui.end_button.setEnabled(True)
        else:
            # Show Inventory
            ui.info_commands.addLayout(ui.inventory_menu)
            ui.draw_inventory(ui.inventory_info)
            ui.invShown = True

            # Disable all direction buttons and End Turn button
            ui.toggle_movement_buttons(False)
            ui.end_button.setEnabled(False)


class EndTurnCommand:
    def __init__(self, ui):
        self.ui = ui

    def process(self):
        ui = self.ui

        # Disable movement and inventory buttons
        ui.toggle_movement_buttons(False)
        ui.toggle_inventory_button(False)
        ui.end_button.setEnabled(False)

        ui.is_player_turn = False  # Set the player's turn to false

        ui.show_enemy_turn()

        if ui.board.player.hit_points > 0:
            ui.new_turn()
        else:
            ui.show_message_box("Game Over", "You Died!")


class MapCommand:
    def __init__(self, ui):
        self.ui = ui
        self.board = ui.board

    def process(self):
        ui = self.ui
        board = ui.board
        player = board.player

        if ui.is_player_turn:  # If it is currently the player's turn, make map clickable
            # Get the current button that had just been clicked
            obj = ui.sender()
            # Get row and column property from the button that was clicked
            row = obj.property("row")
            column = obj.property("column")
            altitude = obj.property("altitude")

            # Get cell property assigned to the current button
            character = obj.property("character")

            if character > 1:  # if click on an enemy
                text = "it is an enemy"

                # Check if the enemy is in range
                board_rows = board.num_rows
                board_cols = board.num_cols

                clicked_loc = (row, column)

                if clicked_loc in Helper.get_adjacent_coordinates(player.x_loc, player.y_loc,
                                                                  board_rows, board_cols):

                    if self.board.player.action_points > 0:  # If there's still AP left
                        text += " and it can be attacked!"
                        enemy_clicked = None
                        for enemy in ui.board.enemies:
                            if enemy.x_loc == row and enemy.y_loc == column:
                                enemy_clicked = enemy

                        # Drop enemy's hp and player's ap
                        enemy.reduce_health(50)
                        player.reduce_action_points(1)
                        # (ui) Updates Health, Action Points and Magic Points for the Player
                        ui.update_info()

                        if player.action_points <= 0:
                            ui.toggle_movement_buttons(False)

                        if enemy.hit_points <= 0:
                            print("Enemy died.")
                            player.notifyObservers("Enemies killed", 1)
                            player.add_gold(enemy.gold)
                            player.notifyObservers("Gold Found", enemy.gold)
                            board.enemies.remove(enemy_clicked)
                            ui.despawn_character(row, column)
                            ui.update_info()
                    else:
                        text += " and it cannot be attacked because you are running out of Action Points!"
                else:
                    text += " and it cannot be attacked because it is out of range!"

            elif (row, column) == board.shop.get_location():
                if (row, column) in Helper.get_adjacent_coordinates(player.x_loc, player.y_loc, board.num_rows,
                                                                    board.num_cols):
                    if ui.invShown:
                        text = 'You can not enter the shop until you close your inventory.'
                    elif ui.shopShown:
                        for row in ui.shop_slot_info:
                            for loc_tuple in row:
                                loc_tuple[2].setIconSize(QSize(0, 0))
                                ui.shop_menu.removeWidget(loc_tuple[2])
                                loc_tuple[2].close()
                        ui.info_commands.removeItem(ui.shop_menu)
                        ui.shopShown = False
                        if player.action_points > 0:
                            ui.toggle_movement_buttons(True)
                        ui.end_button.setEnabled(True)
                        text = 'You have left the shop.'
                    else:
                        ui.info_commands.addLayout(ui.shop_menu)
                        ui.draw_shop(ui.shop_info)
                        ui.shopShown = True

                        ui.toggle_movement_buttons(False)
                        ui.end_button.setEnabled(False)
                        text = 'You have entered the shop.'
                else:
                    text = 'This is the shop. They sell useful items to adventurers like you.'

            else: #Digging
                clicked_loc = (row, column)

                if clicked_loc in Helper.get_adjacent_coordinates(player.x_loc, player.y_loc, board.num_rows,
                                                                  board.num_cols) or clicked_loc == (
                player.x_loc, player.y_loc):
                    if (altitude != 1):
                        text = "You can not dig on this type of terrain."
                    elif player.action_points <= 0:
                        text = "You have no more AP and are too tired to dig."
                    else:
                        player.reduce_action_points(1)
                        player.notifyObservers("Spaces Searched", 1)
                        ui.update_info()
                        x = random.randint(0, 9)

                        if x == 0:
                            ui.inventory.add_to_inventory(ui, 1)
                            ui.draw_inventory(ui.inventory_info)
                            player.notifyObservers("Items Found", 1)
                            text = "Just dug out a bottle of potion!"
                        elif x == 1:
                            player.gold = player.gold + 50
                            ui.update_info()
                            player.notifyObservers("Gold Found", 50)
                            text = "You found 50 Gold!"
                        elif x == 2:
                            player.gold = player.gold + 100
                            ui.update_info()
                            player.notifyObservers("Gold Found", 100)
                            text = "You found 100 Gold!"
                        else:
                            text = "You dug for treasure but found nothing..."

                        if player.action_points <= 0:
                            ui.toggle_movement_buttons(False)
                            ui.toggle_inventory_button(False)
                else:
                    text = "You can not dig here as you are too far away!"
                # text = 'Icon was clicked! Row: ' + str(row + 1) + ', Column: ' + str(column + 1) + ', Altitude: ' + str(altitude) + ', Character: ' + str(character)
            # Generate a message to tell the user the coordinates of the button he/she clicked on
            ui.msg = QMessageBox()
            ui.msg.setWindowTitle("System Message")
            ui.msg.setText(text)
            ui.msg.setIcon(QMessageBox.Information)
            ui.msg.exec()


class ItemCommand:
    def __init__(self, ui):
        self.ui = ui

    def process(self):
        ui = self.ui
        # Get the current button that had just been clicked
        obj = ui.sender()
        # Get row and column property from the current button
        row = obj.property("row")
        column = obj.property("column")
        item_id = obj.property("item_id")

        # Get cell property assigned to the current button
        cell = obj.property("cell")

        # Generate a message to tell the user the coordinates of the button he/she clicked on
        player = ui.board.player

        if item_id == 1:
            player.hit_points = player.hit_points + 25
            text = 'You used a potion! Health increased by 25'

        elif item_id == 2:
            player.action_points = player.action_points + 10
            text = 'You used a chocolate bar! Action points increased by 10'

        elif item_id == 3:
            player.notifyObservers("Enemies killed", 1)
            ui.despawn_character(ui.board.enemies[0].x_loc, ui.board.enemies[0].y_loc)
            ui.board.enemies.remove(ui.board.enemies[0])
            player.magic_points = player.magic_points - 10
            text = 'Killed a nearby enemy!'

        ui.msg = QMessageBox()
        ui.msg.setWindowTitle("")
        ui.msg.setText(text)
        ui.msg.setIcon(QMessageBox.Information)
        ui.msg.exec()
        ui.update_info()
        ui.inventory_info[row][column].set_item_id(0)
        ui.draw_inventory(ui.inventory_info)


class ShopItemCommand:
    def __init__(self, ui):
        self.ui = ui

    def process(self):
        ui = self.ui
        # Get the current button that had just been clicked
        obj = ui.sender()
        # Get row and column property from the current button
        row = obj.property("row")
        column = obj.property("column")
        item_id = obj.property("item_id")

        player = ui.board.player

        # Get cell property assigned to the current button

        # Generate a message to tell the user the coordinates of the button he/she clicked on
        if item_id == 1:
            if ui.last_item_id_clicked == item_id:
                if player.gold >= 50:
                    player = ui.board.player
                    player.gold = player.gold - 50
                    player.notifyObservers("Items purchased", 1)
                    text = 'You spent 50 Gold on a Health Potion!'
                    ui.update_info()
                    ui.inventory.add_to_inventory(ui, 1)
                    ui.shop_info[row][column].set_item_id(0)
                    ui.draw_shop(ui.shop_info)
                else:
                    text = "You don't have enough Gold to purchase this item!"
            else:
                ui.last_item_id_clicked = item_id
                text = 'This is a health potion.\nIncreases HP by 25\nCost: 50 Gold\nClick again to purchase'
        if item_id == 2:
            if ui.last_item_id_clicked == item_id:
                if player.gold >= 25:
                    player = ui.board.player
                    player.gold = player.gold - 25
                    player.notifyObservers("Items purchased", 1)
                    text = 'You spent 25 Gold on a Chocolate Bar!'
                    ui.update_info()
                    ui.inventory.add_to_inventory(ui, 2)
                    ui.shop_info[row][column].set_item_id(0)
                    ui.draw_shop(ui.shop_info)
                else:
                    text = "You don't have enough Gold to purchase this item!"
            else:
                ui.last_item_id_clicked = item_id
                text = 'This is a chocolate bar.\nIncreases AP by 10\nCost: 25 Gold\nClick again to purchase'
        if item_id == 3:
            if ui.last_item_id_clicked == item_id:
                if player.gold >= 100:
                    player = ui.board.player
                    player.gold = player.gold - 100
                    player.notifyObservers("Items purchased", 1)
                    text = 'You spent 100 Gold on a Homing Fireball!'
                    ui.update_info()
                    ui.inventory.add_to_inventory(ui, 3)
                    ui.shop_info[row][column].set_item_id(0)
                    ui.draw_shop(ui.shop_info)
                else:
                    text = "You don't have enough Gold to purchase this item!"
            else:
                ui.last_item_id_clicked = item_id
                text = 'This is a homing fireball.\nKills nearest enemy using 10 MP\nCost: 100 Gold\nClick again to purchase'

        ui.msg = QMessageBox()
        ui.msg.setWindowTitle("")
        ui.msg.setText(text)
        ui.msg.setIcon(QMessageBox.Information)
        ui.msg.exec()


class StatsCommand:
    def __init__(self, ui):
        self.ui = ui

    def process(self):
        ui = self.ui
        stats_list = ui.board.stat_tracker.return_stats()
        stats_str = ""
        for key in stats_list.keys():
            stats_str = stats_str + str(key) + ": " + str(stats_list[key]) + "\n"
        ui.msg = QMessageBox()
        ui.msg.setWindowTitle("Statistics")
        ui.msg.setText(stats_str)
        ui.msg.setIcon(QMessageBox.Information)
        ui.msg.exec()


class NullCommand:
    def __init__(self):
        pass

    def process(self):
        pass
