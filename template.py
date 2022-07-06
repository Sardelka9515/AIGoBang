import sys
sys.path.append(f'{sys.path[0]}/..')
from simplelib import *
from variables import *
import re
import random


def GetNextPoint(board,stone):
  results=[]
  for y in range(len(board)):
    for x in range(len(board)):

      ## empty
      if board[y][x]==0:
        board[y][x]=stone
        result=Result(Score(GetLines(board,stone)),x,y)
        
        # Prevent enemy from winning
        enemyMove=GetBestMove(board,3-stone)
        # enemyMove[1].Print()
        if enemyMove[0]<5 or result.Score>=5:
          # print("original",result.Score)
          result.Score = 1000 if result.Score>=5 else result.Score-enemyMove[0]
          # print("mixed",result.Score)
          results.append(result)
        board[y][x]=0

  
  if len(results)==0:
    # We're doomed
    return Point(random.randint(0,len(board)-1),random.randint(0,len(board)-1))
    
  best=results[0].Score
  for r in results:
    if r.Score>best:
      best=r.Score

  bestResult=RandomResult(results,best)
  # print("score",best)
  return Point(bestResult.X,bestResult.Y)

def GetBestMove(board,stone):
  results=[]
  for y in range(len(board)):
    for x in range(len(board)):
      
      if board[y][x]==0:
        results.append(GetResult(board,x,y,stone))
  if len(results)==0:
    # We're doomed
    return Point(random.randint(0,len(board)),random.randint(0,len(board)))
  
  bestResult=results[0]
  best=results[0].Score
  
  for r in results:
    if r.Score>best:
      best=r.Score
      bestResult=r
  
  return (best,bestResult)

def RandomResult(results,bestScore):
  bestResults=[]
  for r in results:
    if r.Score==bestScore:
      bestResults.append(r)

  return bestResults[random.randint(0,len(bestResults)-1)]
def Score(lines):
  score=-1
  for l in lines:
    s=len(l.Points)
    if(s > score):
      score=s
  # print("score",score)
  return score

def GetResult(board,stepX,stepY,myStone):
  board[stepY][stepX]=myStone
  res= Result(Score(GetLines(board,myStone)),stepX,stepY)
  board[stepY][stepX]=0
  return res
def GetLines(board,stone):
  lines=[]
  for y in range(0,len(board)):
    for x in range(0,len(board)):
      if board[y][x]==stone:
        line=Search1(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),1):
          lines.append(line)

        line=Search2(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),2):
          lines.append(line)

        line=Search3(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),3):
          lines.append(line)

        line=Search4(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),4):
          lines.append(line)
  return lines




class Result:
  def __init__(self,score,x,y):
    self.Score=score
    self.X=x
    self.Y=y

  def Print(self):
    print(self.Score,self.X,self.Y)

def HaveLine(lines,point,dir):
  for line in lines:
        if line.Direction==dir and line.HasPoint(point):
          return True
  return False


# *
#   *
#     *
def Search1(board,point,stone):
  line=[]
  # forward search
  for i in range(0,len(board)-point.Y):
    if point.Y+i>=len(board) or point.X+i>=len(board[0]):
      break;
    if board[point.Y+i][point.X+i] == stone:
      line.append(Point(point.X+i,point.Y+i))
    else:
      break
    # backward
  for i in range(1,point.Y+1):
    if point.Y-i<0 or point.X-i<0:
      break;
    
    if board[point.Y-i][point.X-i] == stone:
      line.insert(0,Point(point.X-i,point.Y-i))
    else:
      break
  return Line(line,1)
  
#     *
#   *
# *    
def Search2(board,point,stone):
  line=[]
# forward search
  for i in range(0,len(board)-point.Y):
    # print("hehe",point.Y+i,point.X-i)
    if point.Y+i>=len(board) or point.X-i<0:
      break;
    if board[point.Y+i][point.X-i] == stone:
      line.append(Point(point.X-i,point.Y+i))
    else:
      break

# backward
  for i in range(1,point.Y+1):
    if point.Y-i<0 or point.X+i>=len(board):
      break;
    # print("checking",point.Y-i,point.X+i)
    if board[point.Y-i][point.X+i] == stone:
      line.insert(0,Point(point.X+i,point.Y-i))
    else:
      break
  return Line(line,2)

#     
# * * *
#     
def Search3(board,point,stone):
  line=[]
# forward search
  for i in range(0,len(board)-point.X):
    if point.X+i>=len(board):
      break;
    if board[point.Y][point.X+i] == stone:
      line.append(Point(point.X+i,point.Y))
    else:
      break

# backward
  for i in range(1,point.X+1):
    if point.X-i<0:
      break;
    if board[point.Y][point.X-i] == stone:
      line.insert(0,Point(point.X-i,point.Y))
    else:
      break
  return Line(line,3)

#   *     
#   *
#   *    
def Search4(board,point,stone):
  line=[]
# forward search
  for i in range(0,len(board)-point.Y):
    if point.Y+i>=len(board):
      break;
    if board[point.Y+i][point.X] == stone:
      line.append(Point(point.X,point.Y+i))
    else:
      break

# backward
  for i in range(1,point.Y+1):
    if point.Y-i<0:
      break;
    if board[point.Y-i][point.X] == stone:
      line.insert(0,Point(point.X,point.Y-i))
    else:
      break
  return Line(line,4)
  


class Point:
  def __init__(self,x,y):
    self.X=x
    self.Y=y
  def GetDir(self,point2):
      if point2.X-self.X==point2.Y-self.Y:
        return 1
      elif point2.X-self.X==-(point2.Y-self.Y):
        return 2
      elif point2.Y==self.Y:
        return 3
      else:
        return 4
  def Equal(self,point):
    return (point.X==self.X) and (point.Y==self.Y)
    
class Line:
  def __init__(self,points,dir):
    self.Points=points
    self.Direction=dir
  
  def HasPoint(self,point):
    for p in self.Points:
      if(p.Equal(point)):
        return True
    return False

def PrintLine(line):
  print("Direction:",line.Direction,end=",")
  for p in line.Points:
    print('(',p.X,',',p.Y,')',end=",")
  print()

import random
testBoard=[
  [1,0,0,2,0],
  [0,1,1,2,1],
  [0,0,1,0,1],
  [0,2,1,0,1],
  [2,0,0,2,2]
]


def GetNextPoint(board,stone):
  results=[]
  for y in range(len(board)):
    for x in range(len(board)):

      ## empty
      if board[y][x]==0:
        board[y][x]=stone
        result=Result(Score(GetLines(board,stone)),x,y)
        
        # Prevent enemy from winning
        enemyMove=GetBestMove(board,3-stone)
        # enemyMove[1].Print()
        if enemyMove[0]<5 or result.Score>=5:
          # print("original",result.Score)
          result.Score = 1000 if result.Score>=5 else result.Score-enemyMove[0]
          # print("mixed",result.Score)
          results.append(result)
        board[y][x]=0

  
  if len(results)==0:
    # We're doomed
    return Point(random.randint(0,len(board)-1),random.randint(0,len(board)-1))
    
  best=results[0].Score
  for r in results:
    if r.Score>best:
      best=r.Score

  bestResult=RandomResult(results,best)
  # print("score",best)
  return Point(bestResult.X,bestResult.Y)

def GetBestMove(board,stone):
  results=[]
  for y in range(len(board)):
    for x in range(len(board)):
      
      if board[y][x]==0:
        results.append(GetResult(board,x,y,stone))
  if len(results)==0:
    # We're doomed
    return Point(random.randint(0,len(board)),random.randint(0,len(board)))
  
  bestResult=results[0]
  best=results[0].Score
  
  for r in results:
    if r.Score>best:
      best=r.Score
      bestResult=r
  
  return (best,bestResult)

def RandomResult(results,bestScore):
  bestResults=[]
  for r in results:
    if r.Score==bestScore:
      bestResults.append(r)

  return bestResults[random.randint(0,len(bestResults)-1)]
def Score(lines):
  score=-1
  for l in lines:
    s=len(l.Points)
    if(s > score):
      score=s
  # print("score",score)
  return score

def GetResult(board,stepX,stepY,myStone):
  board[stepY][stepX]=myStone
  res= Result(Score(GetLines(board,myStone)),stepX,stepY)
  board[stepY][stepX]=0
  return res
def GetLines(board,stone):
  lines=[]
  for y in range(0,len(board)):
    for x in range(0,len(board)):
      if board[y][x]==stone:
        line=Search1(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),1):
          lines.append(line)

        line=Search2(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),2):
          lines.append(line)

        line=Search3(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),3):
          lines.append(line)

        line=Search4(board,Point(x,y),stone)
        if len(line.Points)>1 and not HaveLine(lines,Point(x,y),4):
          lines.append(line)
  return lines




class Result:
  def __init__(self,score,x,y):
    self.Score=score
    self.X=x
    self.Y=y

  def Print(self):
    print(self.Score,self.X,self.Y)

def HaveLine(lines,point,dir):
  for line in lines:
        if line.Direction==dir and line.HasPoint(point):
          return True
  return False


# *
#   *
#     *
def Search1(board,point,stone):
  line=[]
  # forward search
  for i in range(0,len(board)-point.Y):
    if point.Y+i>=len(board) or point.X+i>=len(board[0]):
      break;
    if board[point.Y+i][point.X+i] == stone:
      line.append(Point(point.X+i,point.Y+i))
    else:
      break
    # backward
  for i in range(1,point.Y+1):
    if point.Y-i<0 or point.X-i<0:
      break;
    
    if board[point.Y-i][point.X-i] == stone:
      line.insert(0,Point(point.X-i,point.Y-i))
    else:
      break
  return Line(line,1)
  
#     *
#   *
# *    
def Search2(board,point,stone):
  line=[]
# forward search
  for i in range(0,len(board)-point.Y):
    # print("hehe",point.Y+i,point.X-i)
    if point.Y+i>=len(board) or point.X-i<0:
      break;
    if board[point.Y+i][point.X-i] == stone:
      line.append(Point(point.X-i,point.Y+i))
    else:
      break

# backward
  for i in range(1,point.Y+1):
    if point.Y-i<0 or point.X+i>=len(board):
      break;
    # print("checking",point.Y-i,point.X+i)
    if board[point.Y-i][point.X+i] == stone:
      line.insert(0,Point(point.X+i,point.Y-i))
    else:
      break
  return Line(line,2)

#     
# * * *
#     
def Search3(board,point,stone):
  line=[]
# forward search
  for i in range(0,len(board)-point.X):
    if point.X+i>=len(board):
      break;
    if board[point.Y][point.X+i] == stone:
      line.append(Point(point.X+i,point.Y))
    else:
      break

# backward
  for i in range(1,point.X+1):
    if point.X-i<0:
      break;
    if board[point.Y][point.X-i] == stone:
      line.insert(0,Point(point.X-i,point.Y))
    else:
      break
  return Line(line,3)

#   *     
#   *
#   *    
def Search4(board,point,stone):
  line=[]
# forward search
  for i in range(0,len(board)-point.Y):
    if point.Y+i>=len(board):
      break;
    if board[point.Y+i][point.X] == stone:
      line.append(Point(point.X,point.Y+i))
    else:
      break

# backward
  for i in range(1,point.Y+1):
    if point.Y-i<0:
      break;
    if board[point.Y-i][point.X] == stone:
      line.insert(0,Point(point.X,point.Y-i))
    else:
      break
  return Line(line,4)
  


class Point:
  def __init__(self,x,y):
    self.X=x
    self.Y=y
  def GetDir(self,point2):
      if point2.X-self.X==point2.Y-self.Y:
        return 1
      elif point2.X-self.X==-(point2.Y-self.Y):
        return 2
      elif point2.Y==self.Y:
        return 3
      else:
        return 4
  def Equal(self,point):
    return (point.X==self.X) and (point.Y==self.Y)
    
class Line:
  def __init__(self,points,dir):
    self.Points=points
    self.Direction=dir
  
  def HasPoint(self,point):
    for p in self.Points:
      if(p.Equal(point)):
        return True
    return False

def PrintLine(line):
  print("Direction:",line.Direction,end=",")
  for p in line.Points:
    print('(',p.X,',',p.Y,')',end=",")
  print()


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


def user(board,myStone,remain_time):
  p=GetNextPoint(board,myStone)
  return p.Y,p.X


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
