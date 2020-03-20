from random import randint


class Board:
    def __init__(self, nb_rows, nb_columns, nb_mines):
        self.nb_rows = nb_rows
        self.nb_columns = nb_columns
        self.nb_mines = nb_mines
        self.visible_cells = list('' for _ in range(self.nb_cells()))
        self.__cells = self.__generate_board()

    def dig(self, row, column):
        cell_to_visit = {(row, column)}
        while len(cell_to_visit) != 0:
            (r, c) = cell_to_visit.pop()
            index = self.__get_index(r, c)
            cell = self.__cells[index]
            self.visible_cells[index] = cell
            if cell == 'X':
                break
            elif cell == '0':
                for (next_r, next_c) in self.__get_adjacent_cells(r, c):
                    if not self.__is_visited(next_r, next_c):
                        cell_to_visit.add((next_r, next_c))

    def flag(self, row, column):
        index = self.__get_index(row, column)
        current_cell = self.visible_cells[index]
        if current_cell == 'F':
            self.visible_cells[index] = ''
        elif current_cell == '':
            self.visible_cells[index] = 'F'

    def nb_cells(self):
        return self.nb_rows * self.nb_columns

    def __generate_board(self):
        mines = list(self.__generate_mine_positions())
        return list(self.__compute_cell_score(row, column, mines) for row in range(self.nb_rows) for column in range(self.nb_columns))

    def __generate_mine_positions(self):
        available_mine_positions = list(range(self.nb_cells()))
        for i in range(self.nb_mines):
            mine_pos = randint(0, len(available_mine_positions) - 1)
            yield mine_pos
            del available_mine_positions[mine_pos]

    def __compute_cell_score(self, row, column, mines):
        if self.__get_index(row, column) in mines:
            return 'X'
        else:
            return str(sum(1 if self.__get_index(r, c) in mines else 0 for (r, c) in self.__get_adjacent_cells(row, column)))

    def __get_adjacent_cells(self, row, column):
        row_min = max(row - 1, 0)
        row_max = min(row + 1, self.nb_rows - 1)
        column_min = max(column - 1, 0)
        column_max = min(column + 1, self.nb_columns - 1)
        return list((r, c) for r in range(row_min, row_max + 1) for c in range(column_min, column_max + 1))

    def __get_index(self, row, column):
        return row * self.nb_columns + column

    def __is_visited(self, row, column):
        index = self.__get_index(row, column)
        return self.visible_cells[index] != ''
