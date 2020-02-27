import time
import math
import copy
import random
import json

class Node():
    def __init__(self, board, currentPlace, parentPlace):
        self.board = board
        self.currentPlace = currentPlace
        self.parentPlace = parentPlace


class Game:
    def __init__(self, file):
        self.black_camp = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0],
                           [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2], [4, 0], [4, 1]]
        self.white_camp = [[11, 14], [11, 15], [12, 13], [12, 14], [12, 15], [13, 12], [13, 13], [13, 14], [13, 15],
                           [14, 11], [14, 12], [14, 13], [14, 14], [14, 15], [15, 11], [15, 12], [15, 13], [15, 14],
                           [15, 15]]
        self.mode, self.player, self.timeLimit, self.board = self.readInput(file)

        self.child_path = {}
        self.startTime = 0
        self.endTime = 0
        if self.player == 'B':
            self.origin = [0, 0]
            self.source = self.black_camp
            self.destination = self.white_camp
        else:
            self.origin = [15, 15]
            self.source = self.white_camp
            self.destination = self.black_camp

        self.root = Node(self.board, None, None)
        self.max_time = time.time() + float(self.timeLimit)

        # if self.mode == "GAME":
        #
        #     if self.which_State(self.root) == 'I' or self.which_State(self.root) == 'F':
        #         self.depth = 2
        #         self.max_time = time.time() + 7.0
        #     elif self.which_State(self.root) == 'M':
        #         self.depth = 3
        #         self.max_time = time.time() + 25.0
        #
        #     ans = self.minimax(self.root, self.depth, True)
        #
        # else:
        self.depth = 3
        self.max_flag = True
        ans = self.minimax(self.root, self.depth, True)


        hash_val = hash(str(ans[1]))
        path_str = ''
        if hash_val in self.child_path:
            path = self.child_path[hash_val]

            for i in range(len(path) - 1):
                path_str += ('J ' + str(path[i][1]) + ',' + str(path[i][0]) + ' ' + str(path[i + 1][1]) + ',' + str(
                    path[i + 1][0]) + '\n')
        else:
            path_str = 'E ' + str(ans[1][0][1]) + ',' + str(ans[1][0][0]) + ' ' + str(ans[1][1][1]) + ',' + str(
                ans[1][1][0])

        with open('output.txt', 'w') as file:
            file.write(path_str)

        # print(self.child_path[])

    def readInput(self, file):
        file = open(file, 'r')
        mode = file.readline().strip()
        player = file.readline().strip()[0]
        timeLimit = file.readline().strip()
        board = [[] for i in range(16)]
        for i in range(16):
            line = file.readline().strip()
            for index in range(len(line)):
                board[i].append(line[index])
        return mode, player, timeLimit, board

    def minimax(self, node, depth, max_flag=True, a=float('-inf'), b=float('inf')):
        best_move = Nonex
        eval = self.eval_function(node)
        if depth == 0 or self.win_condition(node) or time.time() > self.max_time:
            return eval, best_move


        if max_flag:
            best_val = float("-inf")
        else:
            best_val = float("inf")

        children = []

        for x in range(16):
            for y in range(16):
                if node.board[x][y] == self.player and [x, y] in self.source:
                    children.extend(self.getChildren(node.board, [x, y]))

        if not children:
            for x in range(16):
                for y in range(16):
                    if node.board[x][y] == self.player and [x, y] not in self.source:
                        children.extend(self.getChildren(node.board, [x, y]))

        random.shuffle(children)
        # children = children[:len(children)//20]
        for child in children:
            if time.time() > self.max_time:
                return best_val, best_move

            val, _ = self.minimax(child, depth - 1, not max_flag, a, b)

            if max_flag and val > best_val:
                best_val = val
                best_move = [child.parentPlace, child.currentPlace]
                if best_val >= b:
                    return best_val, best_move
                a = max(a, val)

            if (not max_flag) and val < best_val:
                best_val = val
                best_move = [child.parentPlace, child.currentPlace]
                if best_val <= a:
                    return best_val, best_move
                b = min(b, val)

            # print(max_flag, child.parentPlace, child.currentPlace, val)
        return best_val, best_move

    def getChildren(self, board, currPlace):

        currPlaceList = [currPlace]
        children = []
        while currPlaceList:
            curr_place = currPlaceList.pop()
            jump_moves = []
            self.jumpMoves(curr_place, board, [], jump_moves)
            for jump_move in jump_moves:

                if jump_move in self.source and curr_place not in self.source:
                    continue

                if jump_move not in self.destination and curr_place in self.destination:
                    continue

                if self.player == 'B':
                    if (curr_place[0] > jump_move[0] or curr_place[1] > jump_move[1]):
                        continue
                else:
                    if (curr_place[0] < jump_move[0] or curr_place[1] < jump_move[1]):
                        continue

                temp_board  = json.loads(json.dumps(board))
                temp_board[jump_move[0]][jump_move[1]] = temp_board[curr_place[0]][curr_place[1]]
                temp_board[curr_place[0]][curr_place[1]] = '.'
                temp_node = Node(temp_board, jump_move, curr_place)
                children.append(temp_node)

            for moves in self.possibleMoves(curr_place):
                move = moves[1]
                if board[move[0]][move[1]] == '.':

                    if move in self.source and curr_place not in self.source:
                        continue

                    if move not in self.destination and curr_place in self.destination:
                        continue



                    if self.player == 'B':
                        if curr_place[0] >= 11 or move[0] >= 11 or curr_place[1] >= 11 or move[1] >= 11:
                            hey = 'hi'
                        else:
                            if (curr_place[0] > move[0] or curr_place[1] > move[1]):
                                continue
                    else:
                        if curr_place[0] <= 4 or move[0] <= 4 or curr_place[1] <= 4 or move[1] <= 4:
                            hey = 'hi'
                        else:
                            if (curr_place[0] < move[0] or curr_place[1] < move[1]):
                                continue

                    temp_board = json.loads(json.dumps(board))
                    temp_board[move[0]][move[1]] = temp_board[curr_place[0]][curr_place[1]]
                    temp_board[curr_place[0]][curr_place[1]] = '.'
                    temp_node = Node(temp_board, move, curr_place)
                    children.append(temp_node)

        return children

    def jumpMoves(self, curr_place, board, visited_nodes, jump_moves, parent=None):
        poss_moves = self.possibleMoves(curr_place)
        for moves in poss_moves:
            move = moves[1]
            if board[move[0]][move[1]] != '.':
                temp_x = curr_place[0] + 2 * (move[0] - curr_place[0])
                temp_y = curr_place[1] + 2 * (move[1] - curr_place[1])
                if -1 < temp_x < 16 and -1 < temp_y < 16:
                    if (board[temp_x][temp_y] == '.' and [temp_x, temp_y] not in visited_nodes) \
                            and (([temp_x, temp_y] in self.source and curr_place in self.source)
                                 or ([temp_x, temp_y] not in self.source and curr_place not in self.source)
                                 or ([temp_x, temp_y] not in self.source and curr_place in self.source)):

                        if ([temp_x, temp_y] in self.source and curr_place in self.source):
                            if self.player == 'B':
                                if (curr_place[0] < temp_x and curr_place[1] < temp_y) \
                                        or (curr_place[0] < temp_x and curr_place[1] == temp_y) \
                                        or (curr_place[0] == temp_x and curr_place[1] < temp_y):
                                    jump_moves.append([temp_x, temp_y])
                                else:
                                    visited_nodes.append([temp_x, temp_y])
                                    continue
                            else:
                                if (curr_place[0] > temp_x and curr_place[1] > temp_y) \
                                        or (curr_place[0] > temp_x and curr_place[1] == temp_y) \
                                        or (curr_place[0] == temp_x and curr_place[1] > temp_y):
                                    jump_moves.append([temp_x, temp_y])
                                else:
                                    visited_nodes.append([temp_x, temp_y])
                                    continue
                        else:
                            jump_moves.append([temp_x, temp_y])
                        # if parent:
                        #     self.child_path[hash(parent[0], [temp_x, temp_y])] = self.child_path[parent].append([temp_x, temp_y])
                        # else:
                        #     self.child_path[hash([curr_place, [temp_x, temp_y]])] = [curr_place, [temp_x, temp_y]]
                        if parent:
                            path = json.loads(json.dumps(self.child_path[hash(str(parent))]))
                            path.append([temp_x, temp_y])
                        else:
                            path = [curr_place, [temp_x, temp_y]]
                        self.child_path[hash(str([path[0], [temp_x, temp_y]]))] = path
                        visited_nodes.append([temp_x, temp_y])
                        self.jumpMoves([temp_x, temp_y], board, visited_nodes, jump_moves, [path[0], [temp_x, temp_y]])
                    else:
                        visited_nodes.append([temp_x, temp_y])

    def possibleMoves(self, currPlace):
        moves = []
        currX, currY = currPlace
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if -1 < currX + x < 16 and -1 < currY + y < 16:
                    if x == 0 and y == 0:
                        continue
                    moves.append([[currX, currY], [currX + x, currY + y]])

        return moves

    def win_condition(self, node):

        opponent = 'W' if self.player == 'B' else 'B'

        count1 = 0
        count2 = 0
        for coors in self.destination:
            if node.board[coors[0]][coors[1]] == opponent:
                count1 += 1
            elif node.board[coors[0]][coors[1]] == self.player:
                count2 += 1
        if count1 == 19:
            return False
        elif count1 + count2 == 19:
            return True
        return False

    def eval_function(self, node):

        if node.currentPlace == None and node.parentPlace == None:
            return 0

        # WIN CONDITION

        if self.win_condition(node):
            return float('inf')

        # if node.currentPlace
        val1 = 0
        val2 = 0
        dest_occupied = 0
        empty_coors = []
        for coors in self.destination:
            if node.board[coors[0]][coors[1]] == self.player:
                dest_occupied += 1
            if node.board[coors[0]][coors[1]] == '.':
                empty_coors.append(coors)

        for row in range(16):
            for col in range(16):
                if node.board[row][col] == self.player:
                    if dest_occupied > 10:
                        if [row, col] not in self.destination:
                            for coors in empty_coors:
                                val2 -= math.sqrt((row - coors[0]) ** 2 + (col - coors[1]) ** 2)
                    else:
                        val1 += math.sqrt((row - self.origin[0]) ** 2 + (col - self.origin[1]) ** 2)

        if(which_State(node) == 'F'):
            
        if dest_occupied > 10:
            return val2
        else:
            return val1

    def which_State(self, node):

        initial = 0
        final = 0
        for coors in self.source:
            if node.board[coors[0]][coors[1]] == self.player:
                initial += 1
        for coors in self.destination:
            if node.board[coors[0]][coors[1]] == self.player:
                final += 1
        if initial >= 10:
            return 'I'
        elif final >= 10:
            return 'F'
        else:
            return 'M'

if __name__ == '__main__':
    # for i in range(1, 7):
    #     file = 'input' + str(i) + '.txt'
    #     game = Game(file)
    x = time.time()
    game = Game('inputG.txt')
    y = time.time()
    print(y - x)
