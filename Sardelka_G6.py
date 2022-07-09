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
  lines=GetLines(board,stone)
  print('found '+str(len(lines))+' on board',file=sys.stderr)
  for l in lines:
    PrintLine(l)
  win1=[]
  lose1=[]
  win2=[]
  lose2=[]
  myMoves=[]
  enemyMoves=[]
  for y in range(len(board)):
    for x in range(len(board)):
      ## empty
      if board[y][x]==0:
        result=GetResult(board,x,y,stone)
        if result.Score>=5:
          
          # print('will win in 1 move',file=sys.stderr)
          win1.append(result)
        elif result.Score==4.5:

          
          # print('will win in 1 move',file=sys.stderr)
          win2.append(result)
        else:
          myMoves.append(result)

  # Predict enemy move
  for y in range(len(board)):
    for x in range(len(board)):
      ## empty
      if board[y][x]==0:
        result=GetResult(board,x,y,3-stone)
        if result.Score>=5:
          # print('will lose in 1 move',file=sys.stderr)
          lose1.append(result)

        elif result.Score==4.5:
          # print('will lose in 2 move',file=sys.stderr)

          lose2.append(result)
        else:
          enemyMoves.append(result)

  if len(win1)!=0:
    # Win
    return RandomResult(win1)

  elif len(lose1)!=0:
    return RandomResult(lose1)

  elif len(win2)!=0:
    return RandomResult(win2)
  
  elif len(lose2)!=0:
    return RandomResult(lose2)

  else:
    results=[]
    for mv in myMoves:
    
      # find best enemy move
      bestEnemyScore=0
      for emv in enemyMoves:
        if emv.X==mv.X and emv.Y==mv.Y:
          continue
        elif emv.Score>bestEnemyScore:
          bestEnemyScore=emv.Score
      mv.Score-=bestEnemyScore
      results.append(mv)

    return RandomResult(results)

def RandomResult(results):
  bestScore=results[0].Score
  bestResults=[]
  for r in results:
    if r.Score==bestScore:
      bestResults.append(r)
    elif r.Score>bestScore:
      bestResults=[]
      bestResults.append(r)
      bestScore=r.Score


  center=Point(7,7)
  closestDist=results[0].DistanceTo(center)
  closestResults=[]
  for r in bestResults:
    d=r.DistanceTo(center)
    if d==closestDist:
      closestResults.append(r)
    elif d<closestDist:
      closestResults=[]
      closestResults.append(r)
      closestDist=d
  if len(closestResults)==1:
    return closestResults[0]
  return closestResults[random.randint(0,len(closestResults)-1)]
  # return bestResults[random.randint(0,len(bestResults)-1)]
def Score(lines,board):
  score=-1
  for l in lines:
    s=len(l.Points)
    if l.Potential(board)==0 and s<5:
      continue
    if l.Potential(board)==2:
      s+=0.5
      # print(str(board[l.Points[0].Y][l.Points[0].X])+"score:"+str(s), file=sys.stderr)
      # PrintBoard(board)
      # time.sleep(100)
    if(s > score):
      score=s
  # print("score",score)
  return score

def GetResult(board,stepX,stepY,myStone):
  
  board[stepY][stepX]=myStone
  res= Result(Score(GetLines(board,myStone),board),stepX,stepY)
  board[stepY][stepX]=0
  return res
def GetLines(board,stone):
  lines=[]
  for y in range(0,len(board)):
    for x in range(0,len(board)):
      if board[y][x]==stone:
        line=Search(board,Point(x,y),stone,Point(1,1))
        if len(line.Points)>1 and not HaveLine(lines,line):
          lines.append(line)

        line=Search(board,Point(x,y),stone,Point(1,-1))
        if len(line.Points)>1 and not HaveLine(lines,line):
          lines.append(line)

        line=Search(board,Point(x,y),stone,Point(1,0))
        if len(line.Points)>1 and not HaveLine(lines,line):
          lines.append(line)

        line=Search(board,Point(x,y),stone,Point(0,1))
        if len(line.Points)>1 and not HaveLine(lines,line):
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

def HaveLine(lines,line):
  for l in lines:
        if l.First==line.First:
          return True
  return False




def Search(board,point,stone,vec):
  line=[]

  i=0
  p=point
  # Forward
  while InRange(p,board) and board[p.Y][p.X]==stone:
    line.append(p)
    i+=1
    p=point+vec*i
  
  i=-1
  p=point+vec*i

  # backward
  while InRange(p,board) and board[p.Y][p.X]==stone:
    line.insert(0,p)
    i-=1
    p=point+vec*i
  
  return Line(line)

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
  def __init__(self,points):
    self.Points=points
    self.First = self.Points[0]
    self.Last = self.Points[len(self.Points)-1]
    if len(self.Points)<=1:
      return
    self.Vec= (self.Last-self.First)/(len(self.Points)-1)
  
  def HasPoint(self,point):
    
    # xinrange = ((self.First.X >= point.X) and (point.X >= self.Last.X)) or ((self.First.X <= point.X) and (point.X <= self.Last.X))
    # yinrange = ((self.First.Y >= point.Y) and (point.Y >= self.Last.Y)) or ((self.First.Y <= point.Y) and (point.Y <= self.Last.Y))

    # return xinrange and yinrange
    for p in self.Points:
      if(p.Equal(point)):
        return True
    return False

  def Potential(self,board):
    
    p1=self.First-self.Vec
    p1.ToInt()
    p2=self.Last+self.Vec
    p2.ToInt()
    potential=int(CanLay(board,p1.X,p1.Y))+int(CanLay(board,p2.X,p2.Y))
    # if potential==2:
      # PrintLine(self)
      # print("\n("+str(p1.X)+','+str(p1.Y)+'),'+'('+str(p2.X)+','+str(p2.Y)+'),',file=sys.stderr)
    return potential

def InRange(point,board):
  x=point.X
  y=point.Y
  size=len(board)
  return (-1 < x) and (x < size) and (-1 < y) and (y < size)
def CanLay(board,x,y):
  size = len (board)
  return (-1 < x) and (x < size) and (-1 < y) and (y < size) and (board[y][x] == 0)
def PrintLine(line):

  for p in line.Points:
    print('('+str(p.X)+','+str(p.Y)+'),',file=sys.stderr,end="")
  print(file=sys.stderr)


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
