import sys
sys.path.append(f'{sys.path[0]}/..')
from simplelib import *
from variables import *
import re

'''
user:
    輸入目前的棋盤跟你是黑棋或白棋(1 or 2)，以及剩餘的時間
    回傳你要下的 index: (row, col)
    param:
        board: list[list[int]]
            board.size == board[0].size == BOARDSIZE
        myStone: int
            myStone in [EMPTY, BLACK, WHITE] (0, 1, 2)
        remain_time: float
            remaining time(unit: second)
    return: row, column
定義請看 variables.py
輔助函式請看 simplelib.py
整個 user 都可以改，除此之外都不要改
NOTE: 若要debug，請使用 print("message", file=sys.stderr)，不要 print 到stdout
'''
#row, col, ldia, rdia = countChain(board,myStone)
#score[i][j] = max(row[i][j], col[i][j], ldia[i][j], rdia[i][j])

def user(board,myStone,remain_time):
  score = [[0 for j in range(BOARDSIZE)] for i in range(BOARDSIZE)] # score 儲存每個格子的分數
  for i in range(BOARDSIZE):
    for j in range(BOARDSIZE): # 遍例每個格子
      if board[i][j] is EMPTY: # 對空的格子算分
        board[i][j] = myStone # 試著下在這格
        a,b,c,d=countChain(board,myStone)
        if max(a[i][j],b[i][j],c[i][j],d[i][j])==5:
          return i , j
        board[i][j] = 3-myStone
        a,b,c,d=countChain(board,3-myStone)
        if max(a[i][j],b[i][j],c[i][j],d[i][j])==5:
          return i , j
        board[i][j] = myStone
        a,b,c,d=countChain(board,myStone)
        if max(a[i][j],b[i][j],c[i][j],d[i][j])==4:
          return i , j
        board[i][j] = 3-myStone
        a,b,c,d=countChain(board,3-myStone)
        if max(a[i][j],b[i][j],c[i][j],d[i][j])==4:
          return i , j
        board[i][j] = myStone
        if i+1<BOARDSIZE and board[i+1][j] == myStone :
          score[i][j]=score[i][j]+1
        if i-1>=0 and board[i-1][j] == myStone :
          score[i][j]=score[i][j]+1
        if j+1<BOARDSIZE and board[i][j+1] == myStone :
          score[i][j]=score[i][j]+1
        if j-1>=0 and board[i][j-1] == myStone :
          score[i][j]=score[i][j]+1
        if i-1>=0 and j+1<BOARDSIZE and board[i-1][j+1] == myStone :
          score[i][j]=score[i][j]+1
        if i+1<BOARDSIZE and j-1>=0 and board[i+1][j-1] == myStone :
          score[i][j]=score[i][j]+1
        if i+1<BOARDSIZE and j+1<BOARDSIZE and board[i+1][j+1] == myStone :
          score[i][j]=score[i][j]+1
        if i-1<=0 and j-1<=0 and board[i-1][j-1] == myStone :
          score[i][j]=score[i][j]+1

        if i+1<BOARDSIZE and board[i+1][j] == 3-myStone :
          score[i][j]=score[i][j]+1
        if i-1>=0 and board[i-1][j] == 3-myStone :
          score[i][j]=score[i][j]+1
        if j+1<BOARDSIZE and board[i][j+1] == 3-myStone :
          score[i][j]=score[i][j]+1
        if j-1>=0 and board[i][j-1] == 3-myStone :
          score[i][j]=score[i][j]+1
        if i-1>=0 and j+1<BOARDSIZE and board[i-1][j+1] == 3-myStone :
          score[i][j]=score[i][j]+1
        if i+1<BOARDSIZE and j-1>=0 and board[i+1][j-1] == 3-myStone :
          score[i][j]=score[i][j]+1
        if i+1<BOARDSIZE and j+1<BOARDSIZE and board[i+1][j+1] == 3-myStone :
          score[i][j]=score[i][j]+1
        if i-1<=0 and j-1<=0 and board[i-1][j-1] == 3-myStone :
          score[i][j]=score[i][j]+1
        board[i][j] = EMPTY # 試完了，拿起來


  
  # 取最大分數的格子回傳
  maxi = 0
  maxj = 0
  max_score = -1
  for i in range(BOARDSIZE):
    for j in range(BOARDSIZE):
      if score[i][j] > max_score:
        max_score = score[i][j]
        maxi = i
        maxj = j
      elif score[i][j] == max_score:
        if abs(i-7)+abs(j-7) < abs(maxi-7)+abs(maxj-7):
          max_score = score[i][j]
          maxi = i
          maxj = j
  # print(maxi, maxj, max_score, file=sys.stderr)
  return maxi, maxj


# DO NOT modify code below!(請絕對不要更改以下程式碼)
# 也可以不用看
def main():
  r = re.compile(r"[^, 0-9-]")
  raw_data = input()
  raw_data = r.sub("",raw_data)
  # print(raw_data)
  user_list = [int(coord) for coord in raw_data.split(', ')]
  # print(user_list)
  input_board = [[]] * 15
  for row in range(15):
    input_board[row] = [0] * 15
  for i in range(15):
    for j in range(15):
      input_board[i][j] = user_list[i*15+j]

  input_mystone = user_list[225]
  remain_t = user_list[226]
  i, j = user(input_board,input_mystone,remain_t)
  print(i,j)


if __name__ == '__main__':
    main()
