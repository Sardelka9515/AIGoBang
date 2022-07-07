import sys
sys.path.append(f'{sys.path[0]}/..')
from simplelib import *
from variables import *
import re
import random

import time

def HavePoint(points,point):
  for p in points:
    if p.Equal(point):
      return True
  return False

def FindPointsToLay(board,stone):
  stones=[]
  for y in range(len(board)):
    for x in range(len(board)):
      if(board[y][x]==stone):
        stones.append(Point(x,y))

  
  foundPoints=[]
  for p in stones:
    FindAmbientPoints(board,foundPoints,p)
  return foundPoints

def FindAmbientPoints(board,points,center):
  p=center
  
  newPoint=Point(p.X+1,p.Y+1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)
      
  newPoint=Point(p.X-1,p.Y-1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)
    
  newPoint=Point(p.X+1,p.Y-1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)
      
  newPoint=Point(p.X-1,p.Y+1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)
    
  newPoint=Point(p.X+1,p.Y+1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)
      
  newPoint=Point(p.X,p.Y+1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)
    
  newPoint=Point(p.X,p.Y-1)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)

  newPoint=Point(p.X+1,p.Y)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)

  newPoint=Point(p.X-1,p.Y)
  if CanLay(board,newPoint.X,newPoint.Y) and not HavePoint(points,newPoint):
    points.append(newPoint)




def GetNextPoint(board,stone):
  # print('(hhhhh),',file=sys.stderr)

  # PrintBoard(board)
  results=[]
  for y in range(len(board)):
    for x in range(len(board)):

      ## empty
      if board[y][x]==0:
        
        # time.sleep(100)
        board[y][x]=stone
        result=Result(Score(GetLines(board,stone),board),x,y)
        
        # Predict enemy move
        enemyMove=GetBestMove(board,3-stone)
        # print('(hhssshhh),',file=sys.stderr)

        # enemyMove[1].Print()
        if enemyMove[0]<5:
          if result.Score>=5:
            result.Score = 1000
          elif enemyMove[0] == 4.5 and result.Score!=4.5:
            result.Score-=(enemyMove[0]+5)
          else:
            result.Score-=enemyMove[0]
          # print("original",result.Score)
          # print("mixed",result.Score)
        elif result.Score>=5:
          result.Score = 1000
        else:
          result.Score=-100
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
  for p in FindPointsToLay(board,stone):
    results.append(GetResult(board,p.X,p.Y,stone))

  if len(results)==0:
    
    return (0,Result(0,0,0))
  
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

  center=Point(7.5,7.5)
  closetResult=0
  closetDist=1000000
  for r in bestResults:
    d=r.DistanceTo(center)
    if d<closetDist:
      closetResult=r
      closetDist=d
  
  return closetResult
  # return bestResults[random.randint(0,len(bestResults)-1)]
def Score(lines,board):
  score=-1
  for l in lines:
    s=len(l.Points)
    if s == 4 and l.Potential(board)==2:
      s+=0.5
      # print(str(board[l.Points[0].Y][l.Points[0].X])+"score:"+str(s), file=sys.stderr)
      # PrintBoard(board)
      # time.sleep(100)
    if(s > score and not l.IsDead(board)):
      score=s
  # print("score",score)
  return score

def GetResult(board,stepX,stepY,myStone):
  
  board[stepY][stepX]=myStone
  lines=GetLines(board,myStone)
  res= Result(Score(lines,board),stepX,stepY)
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
def PrintBoard(board):
  for r in board:
    for c in r:
      print(c,file=sys.stderr,end="")
    print("",file=sys.stderr)
     


class Result:
  def __init__(self,score,x,y):
    self.Score=score
    self.X=x
    self.Y=y

  def Print(self):
    print(self.Score,self.X,self.Y)
  
  def DistanceTo(self,point):
    return (self.X-point.X)**2+(self.Y-point.Y)**2

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

  def __add__(self,p):
    return Point(self.X+p.X,self.Y+p.Y)

  def __sub__(self,p):
    return Point(self.X-p.X,self.Y-p.Y)

  def __mul__(self,i):
    return Point(self.X*i,self.Y*i)

  def __neg__(self):
    return Point(self.X*-1,self.Y*-1)

  def __eq__(self,p):
    return self.X == p.X and self.Y == p.Y

  def __truediv__(self,i):
    return Point(self.X/i,self.Y/i)
  
  def ToInt(self):
    self.X=int(self.X)
    self.Y=int(self.Y)
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

  def Potential(self,board):
    first = self.Points[0]
    last = self.Points[len(self.Points)-1]
    vec= (last-first)/(len(self.Points)-1)
    p1=first-vec
    p1.ToInt()
    p2=last+vec
    p2.ToInt()
    potential=int(CanLay(board,p1.X,p1.Y))+int(CanLay(board,p2.X,p2.Y))
    # if potential==2:
      # PrintLine(self)
      # print("\n("+str(p1.X)+','+str(p1.Y)+'),'+'('+str(p2.X)+','+str(p2.Y)+'),',file=sys.stderr)
    return potential
  def IsDead(self,board):
    if(len(self.Points)>=5):
      return False
    first = self.Points[0]
    last = self.Points[len(self.Points)-1]
    if self.Direction == 1:
      return not(CanLay(board,first.X-1,first.Y-1) or CanLay(board,last.X+1,last.Y+1))
    elif self.Direction == 2:
      return not(CanLay(board,first.X+1,first.Y-1) or CanLay(board,last.X-1,last.Y+1))
    elif self.Direction == 3:
      return not(CanLay(board,first.X-1,first.Y) or CanLay(board,last.X+1,last.Y))
    elif self.Direction == 4:
      return not(CanLay(board,first.X,first.Y-1) or CanLay(board,last.X,last.Y+1))
    else:
      return False

def CanLay(board,x,y):
  size = len (board)
  return (-1 < x) and (x < size) and (-1 < y) and (y < size) and (board[y][x] == 0)
def PrintLine(line):

  for p in line.Points:
    print('('+str(p.X)+','+str(p.Y)+'),',file=sys.stderr,end="")
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
