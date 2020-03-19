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

class Button:
    def __init__(self, label, x, y, action):
        self.label = label
        self.x = x
        self.y = y
        self.action = action

    def update(self):
        x = pyxel.mouse_x
        y = pyxel.mouse_y
        is_clicked = self.x <= x and self.x + BUTTON_WIDTH >= x and self.y <= y and self.y + BUTTON_HEIGHT >= y
        if is_clicked:
            return self.action()

    def draw(self):
        pyxel.rect(self.x, self.y, BUTTON_WIDTH, BUTTON_HEIGHT, 2)
        pyxel.text(self.x + (BUTTON_WIDTH - len(self.label) * 4) // 2, self.y + BUTTON_LABEL_Y, self.label, 0)

class Cell:
    def __init__(self, x, y, action):
        self.x = x
        self.y = y
        self.action = action

    def update(self):
        x = pyxel.mouse_x
        y = pyxel.mouse_y
        is_clicked = self.x <= x and self.x + CELL_SIZE >= x and self.y <= y and self.y + CELL_SIZE >= y
        if is_clicked:
            return self.action()

    def draw(self, label):
        pyxel.rect(self.x, self.y, CELL_SIZE, CELL_SIZE, 2)
        pyxel.rectb(self.x, self.y, CELL_SIZE, CELL_SIZE, 0)
        pyxel.text(self.x + 2, self.y + 1, label, 0)

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, caption="Minesweeper")
        pyxel.mouse(True)

        self.__screen = 'home'

        self.__home_buttons = [
            Button('Easy', BUTTON_X, BUTTON_Y, lambda: Board(8, 10, 10)),
            Button('Medium', BUTTON_X, BUTTON_Y + BUTTON_HEIGHT + BUTTON_Y_MARGIN, lambda: Board(14, 18, 40)),
            Button('Hard', BUTTON_X, BUTTON_Y + 2 * (BUTTON_HEIGHT + BUTTON_Y_MARGIN), lambda: Board(20, 24, 99))
        ]

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
                    cell = cell.update()
                    if cell == 'X':
                        self.__screen = 'end'
                        break

    def __draw(self):
        pyxel.cls(1)
        if self.__screen == 'home': 
            pyxel.text(58, 35, 'Minesweeper', pyxel.frame_count % 16)
            for button in self.__home_buttons:
                button.draw()
        elif self.__screen == 'game':
            for index in range(len(self.__cells)):
                label = self.__board.visible_cells[index]
                self.__cells[index].draw(label)
        else:
            pyxel.text(58, 35, 'Bouh loser', pyxel.frame_count % 16)

    def __create_cells(self):
        self.__cells = list(self.__create_cell(index) for index in range(len(self.__board.visible_cells)))

    def __create_cell(self, index):
        column = index % self.__board.nb_columns
        row = index // self.__board.nb_columns
        offset_x = (WIDTH - self.__board.nb_columns * CELL_SIZE) // 2
        offset_y = (HEIGHT - self.__board.nb_rows * CELL_SIZE) // 2
        x = column * CELL_SIZE + offset_x
        y = row * CELL_SIZE + offset_y
        return Cell(x, y, lambda: self.__board.dig(row, column))
