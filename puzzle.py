from tkinter import Frame, Label, CENTER
import random
import logic 
import constants as c
# import numpy as nu


# def sigmoid(x):
#     return 1. / (1. + np.exp(-x))


def gen():
    return random.randint(0, c.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.score = []
        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.history_matrixs.append(self.matrix)
        self.update_grid_cells()
        # self.mainloop()
        
    def init_grid(self):
        global score
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()
        for i in range(c.GRID_LEN+1):
            grid_row = []
            if i < 4:
                for j in range(c.GRID_LEN):
                    cell = Frame(
                        background,
                        bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                        width=c.SIZE / c.GRID_LEN,
                        height=c.SIZE / c.GRID_LEN
                    )
                    cell.grid(
                        row=i,
                        column=j,
                        padx=c.GRID_PADDING,
                        pady=c.GRID_PADDING
                    )
                    t = Label(
                        master=cell,
                        text="",
                        bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                        justify=CENTER,
                        font=c.FONT,
                        width=5,
                        height=2)
                    t.grid()
                    grid_row.append(t)
                self.grid_cells.append(grid_row)
            else:
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=4,
                    column=0,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text=str(logic.score),
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    fg="#eee4da",
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
                self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.grid_cells[4][0].configure(
            text=str(logic.score),
            bg=c.BACKGROUND_COLOR_CELL_EMPTY,
            fg="#eee4da",
        )
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        print(event.keysym)
        if key == c.KEY_QUIT:
            exit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.history_matrixs.pop()
            self.matrix = self.history_matrixs.pop()
            self.score.pop()
            logic.score = self.score.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.score.append(logic.score)
                self.update_grid_cells()
                # if logic.game_state(self.matrix) == 'win':
                # self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                # self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                # if logic.game_state(self.matrix) == 'lose':
                # self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                # self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def input_command(self, key):
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            logic.score = self.score.pop()
            self.update_grid_cells()
            # print('back on step total step:', len(self.history_matrixs))
        else:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add(self.matrix)
                self.history_matrixs.append(self.matrix)
                self.score.append(logic.score)
                self.update_grid_cells()


class Player(GameGrid):
    def __init__(self):
        self.game = GameGrid()

    def training(self):
        way = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
        w = []
        p = 0
        k = -1
        go_on = True
        weight = 0
        while p < 1000 and go_on:
            out = []
            for i in range(4):
                if p != 0 and i == k:
                    w.append(weight)
                else:
                    w.append(Weight())
            for text in way:
                self.game.input_command(text)
                out.append(logic.score)
                self.game.input_command(c.KEY_BACK)
            Sum = 0
            Max = max(out)
            for i in range(4):
                Sum += out[i]
                if out[i] == Max:
                    k = i
            for i in range(4):
                weight += w[i].weight*out[i]/Sum
            self.game.input_command(way[k])
            if logic.game_state(self.game.matrix) == 'lose':
                go_on = False
                print(logic.score)


class Weight():
    def __init__(self):
        self.weight = []
        self.weight_init()

    def weight_init(self):
        row = []
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                row.append(random.random())
            self.weight.append(row)


ai = Player()
ai.training()
ai.game.mainloop()
