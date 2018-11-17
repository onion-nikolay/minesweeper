"""
@author: onion-nikolay
"""

import numpy as np
from timeit import default_timer as timer

STATUS_SYMB = {-3: '??', -2: '!!', -1: "xx", 0: ' 0', 1: ' 1', 2: ' 2',
               3: ' 3', 4: ' 4', 5: ' 5', 6: ' 6', 7: ' 7', 8: ' 8'}


def calcMinesNum(field, coord):
    coord_1 = [x for x in [coord[0]-1, coord[0], coord[0]+1] if (
            (x >= 0) and (x < np.shape(field)[0]))]
    coord_2 = [x for x in [coord[1]-1, coord[1], coord[1]+1] if (
            (x >= 0) and (x < np.shape(field)[1]))]
    num = 0
    for x in coord_1:
        for y in coord_2:
            num += field[x, y]
    return num


def endOfGame(win=False):
    if win:
        print("End of game. You won!")
    else:
        print("End of game. You lost!")
    input()
    return False


def generateField(field_size=[16, 16], number_of_mines=40,
                  first_coord=[-1, -1]):
    field = np.zeros(field_size, dtype=int)
    mines_defined = 0
    while mines_defined < number_of_mines:
        coord = [np.random.randint(0, field_size[0]),
                 np.random.randint(0, field_size[1])]
        if (field[coord[0], coord[1]] == 0 and coord != first_coord):
            field[coord[0], coord[1]] = 1
            mines_defined += 1
    return field


def session():
    print("Input size of field (example: 16 16)")
    raw_field_size = input()
    field_size = [int(s) for s in raw_field_size.split() if s.isdigit()]
    print("Input number of mines")
    raw_number_of_mines = input()
    number_of_mines = int(raw_number_of_mines)
    showEmptyField(field_size, number_of_mines)
    print("Input 'x y' for first click.")
    start = timer()
    raw_first_click = input()
    first_click = [int(s)-1 for s in raw_first_click.split() if s.isdigit()]
    gm = game(field_size, number_of_mines, first_click)
    print("For click, print 'x y'. For mark, print 'mark x y'. Good luck!")
    while (gm.inprocess):
        rawinput = input()
        _input = rawinput.split()
        if _input != []:
            if _input[0] == 'mark':
                try:
                    gm.mark([int(_input[1])-1, int(_input[2])-1])
                except ValueError:
                    pass
            else:
                try:
                    gm.click([int(_input[0])-1, int(_input[1])-1])
                except ValueError:
                    pass
            mask = (gm.status == -1)
            print("Mines: {}/{}".format(np.sum(mask), number_of_mines))
            if ((mask == gm.field).min() and (np.sum(mask) == number_of_mines)
                    and not((gm.status == -3).max())):
                gm.inprocess = endOfGame(True)
    time = timer() - start
    print("Elapsed time: {}m{}s.\n".format(int(time/60),
          int(time-60*int(time/60))))
    return 0


def showEmptyField(field_size, number_of_mines):
    [ylen, xlen] = field_size
    s = '  |'
    for x in range(xlen):
        s += ('%.2d' % (x+1))
        s += '|'
    print(s)
    for y in range(ylen):
        s = ('%.2d' % (y+1))
        for x in range(xlen):
            s = s + '|' + STATUS_SYMB[-3]
        s = s + '|'
        print(s)


class game:
    def __init__(self, field_size, number_of_mines, *first_click):
        try:
            first_coord = first_click[0]
        except IndexError:
            first_coord = [-1, -1]
        self.field = generateField(field_size, number_of_mines, *first_click)
        self.seen = np.zeros(field_size)
        self.status = np.ones(field_size)*-3
        self.inprocess = True
        self.click(first_coord)

    def click(self, coord):
        x = coord[0]
        y = coord[1]
        if self.seen[x, y] == 1:
            self.show()
            return
        self.seen[x, y] = 1
        if self.field[x, y] == 1:
            self.status[x, y] = -2
            self.show()
            self.inprocess = endOfGame()
            return
        self.status[x, y] = calcMinesNum(self.field, coord)
        self.show()
        return

    def mark(self, coord):
        x = coord[0]
        y = coord[1]
        if self.seen[x, y] == 1:
            if self.status[x, y] == -1:
                self.status[x, y] = -3
                self.seen[x, y] = 0
            else:
                return
        else:
            self.seen[x, y] = 1
            self.status[x, y] = -1
        self.show()
        return

    def show(self):
        [ylen, xlen] = np.shape(self.field)
        s = '  |'
        for x in range(xlen):
            s += ('%.2d' % (x+1))
            s += '|'
        print(s)
        for y in range(ylen):
            s = ('%.2d' % (y+1))
            for x in range(xlen):
                s = s + '|' + STATUS_SYMB[self.status[y, x]]
            s = s + '|'
            print(s)


if __name__ == '__main__':
    __inprocessing = True
    while __inprocessing:
        session()
        print("Try again? (print 'y')")
        __answer = input()
        if __answer == 'y':
            pass
        else:
            __inprocessing = False
            print("Goodbye!")
