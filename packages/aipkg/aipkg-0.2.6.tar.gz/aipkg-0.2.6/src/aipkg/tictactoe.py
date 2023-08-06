from typing import List
import time

class TicTacToe:
    def __init__(self, computer: str, human: str, turn: bool, optimize: bool =True) -> None:
        self.computer = computer
        self.human = human
        self.board = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
        self.turn = computer
        self.optmize = optimize
        self.timestamps = []

    def changeTurn(self):
        if self.turn:
            self.turn = 0
        else:
            self.turn = 1

    def board_not_full(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return True
        return False

    def printBoard(self,move: str,pos: List[int]):
        x = pos[0]
        y = pos[1]

        if self.board[x][y] == ' ':
            self.board[x][y] = move
            self.changeTurn()
        else:
            raise Exception("Invalid move. Try again")

        for i in range(3):
            for j in range(3):
                print(" "+self.board[i][j]+"|",end='')
            print()
        print("----------------------------------------")

    def utility_function(self):

        for row in range(3):
            if self.board[row][0] == self.board[row][1] and self.board[row][1] == self.board[row][2]:
                if self.board[row][0] == self.computer:
                    return 1
                elif self.board[row][0] == self.human:
                    return -1

        for col in range(3):
            if self.board[0][col] == self.board[1][col] and self.board[1][col] == self.board[2][col]:
                if self.board[0][col] == self.computer:
                    return 1
                if self.board[0] == self.human:
                    return -1

        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == self.computer:
                return 1
            if self.board[0][0] == self.human:
                return -1

        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == self.computer:
                return 1
            if self.board[0][2] == self.human:
                return -1

        return 0

    def minimax(self, depth: int, maxTurn: bool, alpha:int =-1, beta:int =1):
        score = self.utility_function()

        if score == 1:
            return score

        if score == -1:
            return score

        if not self.board_not_full():
            return 0

        if maxTurn:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.computer
                        best = max(best, self.minimax(depth+1, False))
                        self.board[i][j] = ' '

                        if self.optimize:
                            if best >= beta:
                                return best
                            if best > alpha:
                                alpha = best
            return best
        else:
            best =-1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.computer
                        best = min(best, self.minimax(depth+1, True))
                        self.board[i][j] = ' '

                        if self.optimize:
                            if best <= alpha:
                                return best
                            if best < beta:
                                beta = best
            return best

    def bestMove(self):
        bestVal = -1000
        best_move = [-1,-1]

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.computer
                    moveVal = self.minimax(0, False)

                    self.board[i][j] = ' '

                    if moveVal > bestVal:
                        best_move = [i,j]
                        bestVal = moveVal
        return best_move

    def game_start(self):

        while self.board_not_full():

            if self.utility_function() == 1:
                print(f"{self.computer} wins")
                return
            if self.utility_function() == -1:
                print(f"{self.human} wins")
                return

            if self.turn:
                start = time.time()
                pos = self.bestMove()
                self.timestamps.append(f"{round(time.time()-start,5)} seconds")
                print(f"Evaluation time: {round(time.time()-start,5)} seconds")
                self.printBoard(self.computer,pos)
            else:
                pos = input("Enter your move: ")
                self.printBoard(self.human,pos)
        if self.utility_function() == 1:
            print(f"{self.computer} wins")
            return
        elif self.utility_function() == -1:
            print(f"{self.human} wins")
            return
        else:
            print("It's a draw")