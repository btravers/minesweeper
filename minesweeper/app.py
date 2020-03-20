import pyxel

from board import Board

# CONSTANTS

WIDTH = 160
HEIGHT = 120

BUTTON_WIDTH = 31
BUTTON_HEIGHT = 11
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = 55
BUTTON_Y_MARGIN = 3
BUTTON_LABEL_Y = 3

CELL_SIZE = 7


class Clickable:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height

    def is_clicked(self):
        return self.x <= pyxel.mouse_x and self.x + self.__width >= pyxel.mouse_x and self.y <= pyxel.mouse_y and self.y + self.__height >= pyxel.mouse_y


class Button(Clickable):
    def __init__(self, label, x, y, action):
        self.__label = label
        self.__action = action

        Clickable.__init__(self, x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def update(self):
        if self.is_clicked():
            return self.__action()

    def draw(self):
        pyxel.rect(self.x, self.y, BUTTON_WIDTH, BUTTON_HEIGHT, 2)
        pyxel.text(self.x + (BUTTON_WIDTH - len(self.__label) * 4) //
                   2, self.y + BUTTON_LABEL_Y, self.__label, 0)


class Cell(Clickable):
    def __init__(self, x, y, left_click, right_click):
        self.__left_click = left_click
        self.__right_click = right_click

        Clickable.__init__(self, x, y, CELL_SIZE, CELL_SIZE)

    def left_click(self):
        if self.is_clicked():
            return self.__left_click()

    def right_click(self):
        if self.is_clicked():
            return self.__right_click()

    def draw(self, label):
        pyxel.rect(self.x, self.y, CELL_SIZE, CELL_SIZE, 3)
        pyxel.rectb(self.x, self.y, CELL_SIZE, CELL_SIZE, 0)
        pyxel.text(self.x + 2, self.y + 1, label, self.__get_color(label))

    def __get_color(self, label):
        if label == 'F':
            return 4
        else:
            return 5


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, caption="Minesweeper")
        pyxel.mouse(True)

        self.__screen = 'home'

        self.__home_buttons = [
            Button('Easy', BUTTON_X, BUTTON_Y, lambda: Board(8, 10, 10)),
            Button('Medium', BUTTON_X, BUTTON_Y + BUTTON_HEIGHT +
                   BUTTON_Y_MARGIN, lambda: Board(14, 18, 40)),
            Button('Hard', BUTTON_X, BUTTON_Y + 2 * (BUTTON_HEIGHT +
                                                     BUTTON_Y_MARGIN), lambda: Board(20, 24, 99))
        ]
        self.__restart_button = Button(
            'Restart', BUTTON_X, BUTTON_Y, lambda: True)

        pyxel.run(self.__update, self.__draw)

    def __update(self):
        if self.__screen == 'home':
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                for button in self.__home_buttons:
                    board = button.update()
                    if board != None:
                        self.__board = board
                        self.__create_cells()
                        self.__screen = 'game'
                        break
        elif self.__screen == 'game':
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                for cell in self.__cells:
                    cell.left_click()

                if self.__is_win():
                    self.__screen = 'win'

                if self.__is_lose():
                    self.__screen = 'lose'
            if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
                for cell in self.__cells:
                    cell.right_click()
        else:
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                if self.__restart_button.update():
                    self.__screen = 'home'

    def __draw(self):
        pyxel.cls(1)
        if self.__screen == 'home':
            pyxel.text(58, 35, 'Minesweeper', pyxel.frame_count % 16)
            for button in self.__home_buttons:
                button.draw()
        elif self.__screen == 'game':
            self.__draw_cells()
        elif self.__screen == 'win':
            self.__draw_cells()
            pyxel.text(65, 35, 'You win', pyxel.frame_count % 16)
            self.__restart_button.draw()
        else:
            self.__draw_cells()
            pyxel.text(58, 35, 'Bouh loser', pyxel.frame_count % 16)
            self.__restart_button.draw()

    def __create_cells(self):
        self.__cells = list(self.__create_cell(index)
                            for index in range(len(self.__board.visible_cells)))

    def __create_cell(self, index):
        column = index % self.__board.nb_columns
        row = index // self.__board.nb_columns
        offset_x = (WIDTH - self.__board.nb_columns * CELL_SIZE) // 2
        offset_y = (HEIGHT - self.__board.nb_rows * CELL_SIZE) // 2
        x = column * CELL_SIZE + offset_x
        y = row * CELL_SIZE + offset_y
        return Cell(x, y, lambda: self.__board.dig(row, column), lambda: self.__board.flag(row, column))

    def __draw_cells(self):
        for index in range(len(self.__cells)):
            label = self.__board.visible_cells[index]
            self.__cells[index].draw(label)

    def __is_win(self): 
        nb_discovered_cells = sum(0 if c == '' or c == 'F' else 1 for c in self.__board.visible_cells)
        nb_cells_to_discover = self.__board.nb_cells() - self.__board.nb_mines
        print(nb_discovered_cells)
        print(nb_cells_to_discover)
        return nb_discovered_cells == nb_cells_to_discover

    def __is_lose(self):
        return any(c == 'X' for c in self.__board.visible_cells)
