from __future__ import with_statement
import time
import os
import homework2

class Handler:
    def __init__(self):
        self.black_camp = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0],
                           [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2], [4, 0], [4, 1]]
        self.white_camp = [[11, 14], [11, 15], [12, 13], [12, 14], [12, 15], [13, 12], [13, 13], [13, 14], [13, 15],
                           [14, 11], [14, 12], [14, 13], [14, 14], [14, 15], [15, 11], [15, 12], [15, 13], [15, 14],
                           [15, 15]]

        self.player = 'WHITE'
        self.mode = 'GAME'
        self.time = 300
        self.board = [['.' for i in range(16)] for j in range(16)]
        self.time1 = 0
        self.time2 = 0
        self.moves = 0
        for i in range(16):
            for j in range(16):
                if [i, j] in self.black_camp:
                    self.board[i][j] = 'B'
                elif [i, j] in self.white_camp:
                    self.board[i][j] = 'W'



    def writeFile(self):
        with open('input.txt', 'w') as infile:
            boardStr = ""

            # os.system('clear')
            for i in range(16):
                temp = ""
                for j in range(16):
                    boardStr += (self.board[i][j])
                    temp += self.board[i][j]
                # print(temp)
                boardStr += ('\n')
            # print()
            # print()
            opponent = 'BLACK' if flag % 2 == 0 else 'WHITE'
            outString = self.mode + "\n" + opponent + '\n' + str(self.time) + "\n" + boardStr + str(self.time1) + '\n' + str(self.time2) + '\n' + str(self.moves)

            infile.write(outString)

    def win(self):

        opponent = 'W' if self.player[0] == 'B' else 'B'

        destination = self.white_camp if self.player[0] == 'B' else self.black_camp
        count1 = 0
        count2 = 0
        for coors in destination:
            if self.board[coors[0]][coors[1]] == opponent:
                count1 += 1
            elif self.board[coors[0]][coors[1]] == self.player[0]:
                count2 += 1
        if count1 == 19:
            return False
        elif count1 + count2 == 19:
            return True
        return False


if __name__ == '__main__':

    handler = Handler()
    try:

        with open('input.txt', 'r') as file:
        # file = open('input.txt', 'r')
            file.readline()
            player = file.readline().strip()
            time_rem = file.readline().strip()
            board_str = file.readline().strip()
            for _ in range(15):
                board_str += file.readline().strip()
            index = 0
            board = [['.' for i in range(16)] for j in range(16)]

            for i in range(len(board_str)):
                board[i // 16][i % 16] = board_str[i]

            handler.board = board
            handler.player = player
            handler.time = time_rem
        # file.close()
    except (OSError, IOError) as e:
        handler.initBoard()
        handler.writeFile()

    os.system('javac homework.java')

    win = False
    # count = 0
    flag = 0
    time1 = 0
    time2 = 0
    while not handler.win():
        with open('output.txt', 'w') as trunc:
            trunc.truncate(0)
        if flag % 2 == 0:
            start = time.time()
            handler.player = 'WHITE'
            homework2.Game('input.txt')
            time1 += time.time() - start
            handler.time1 = time1
            # print()
        else:
            start = time.time()
            handler.player = 'BLACK'
            os.system('java homework')
            time2 += time.time() - start
            handler.time2 = time2
        with open('output.txt', 'r') as file:
            line = file.readline().strip()
            if line[0] == 'E':
                move = line.split()
                fro = move[1].split(',')
                to = move[2].split(',')
            else:
                lines = [line]
                lines.extend(file.readlines())
                # print(lines)
                first = lines[0].strip().split()[1]
                last = lines[-1].strip().split()[2]

                # move1 = first.split()
                fro = first.split(',')

                # move2 = last.split()
                to = last.split(',')

            handler.board[int(fro[1])][int(fro[0])] = '.'
            handler.board[int(to[1])][int(to[0])] = 'W' if flag % 2 == 0 else 'B'
            handler.writeFile()

        flag += 1
        handler.moves = flag
        # time.sleep(0.75)