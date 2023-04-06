from PySide6 import QtGui
from PySide6.QtCore import QSize


def image_merge(background_image_path, foreground_image_path) -> QtGui.QPixmap:
    image = QtGui.QPixmap(50, 50)

    background = QtGui.QImage(background_image_path).scaled(50, 50)
    foreground = QtGui.QImage(foreground_image_path).scaled(25, 25)

    painter = QtGui.QPainter()

    painter.begin(image)
    painter.drawImage(0, 0, background)
    painter.drawImage(12.5, 12.5, foreground)
    painter.end()
    return image


def assign_texture(pixmap, button):
    pixmap = pixmap.scaled(50, 50)
    button.setIcon(pixmap)
    button.setIconSize(QSize(50, 50))


def get_adjacent_coordinates(x_loc, y_loc, num_rows, num_cols):

    adjacent_cells = []

    for x in range(x_loc - 1, x_loc + 2, 1):
        for y in range(y_loc - 1, y_loc + 2, 1):

            if not (x_loc == x and y_loc == y) and (0 <= x < num_cols) and (0 <= y < num_rows):
                adjacent_cells.append((x, y))
    return adjacent_cells


def get_cardinal_coordinates(x_loc, y_loc, num_rows, num_cols):

    adjacent_coords = [(x_loc, y_loc - 1), (x_loc, y_loc + 1), (x_loc - 1, y_loc), (x_loc + 1, y_loc)]
    feasible_cells = []

    for coord in adjacent_coords:
        if (0 <= coord[0] < num_cols) and (0 <= coord[1] < num_rows):
            feasible_cells.append(coord)

    return feasible_cells


def get_next_coordinates(direction, current_loc):
    current_x_loc, current_y_loc = current_loc

    if direction == 'up':
        return current_x_loc - 1, current_y_loc
    elif direction == 'down':
        return current_x_loc + 1, current_y_loc
    elif direction == 'left':
        return current_x_loc, current_y_loc - 1
    elif direction == 'right':
        return current_x_loc, current_y_loc + 1
