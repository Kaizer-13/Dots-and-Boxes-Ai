import copy
import sys

fx=[1,-1,0,0]
fy=[0,0,1,-1]

cx=[-1,-1,0,0]
cy=[-1,0,-1,0]

sx1=[0,1,0,0]
sy1=[0,0,0,1]
mv=[2,2,0,0]

size=2
total=size*size


def isFinish(scores):
    for i in range(size-1):
        for j in range(size-1):
            if scores[i][j]==-1:
                return 0
    return 1

def valid(x,y,sz):
    if x>=0 and x<sz and y>=0 and y<sz:
        return 1
    else: 
        return 0
            
def gotScore(i,j,lines,scores):

    found = 0 
    for x in range(4):
        found_this=1
        sqi=i+cx[x]
        sqj=j+cy[x]
        if valid(sqi,sqj,size-1) and scores[sqi][sqj]==-1:
            for y in range(4):
                cornerX1=sqi+sx1[y]
                cornerY1=sqj+sy1[y]
                mvIdx=mv[y]
                pVal1=cornerX1*size+cornerY1
                if lines[pVal1][mvIdx]!=1:
                    found_this=0
                    break
        if valid(sqi,sqj,size-1) and scores[sqi][sqj]==-1 and found_this==1:
            found=1
    return found


def putScore(i,j,lines,scores,value):
    for x in range(4):
        found_this=1
        sqi=i+cx[x]
        sqj=j+cy[x]
        if valid(sqi,sqj,size-1) and scores[sqi][sqj]==-1:
            for y in range(4):
                cornerX1=sqi+sx1[y]
                cornerY1=sqj+sy1[y]
                mvIdx=mv[y]
                pVal1=cornerX1*size+cornerY1
                if lines[pVal1][mvIdx]!=1:
                    found_this=0
                    break
        if valid(sqi,sqj,size-1) and scores[sqi][sqj]==-1 and found_this==1:
            scores[sqi][sqj]=value

count = 0

def minimax(lines, scores, isMaxplayer):
    global count
    count=count+1
    if isFinish(scores)==1:
        value=0
        for i in range(size-1):
            for j in range(size-1):
                score=scores[i][j]
                if score==2:
                    value=value-1
                elif score==1:
                    value=value+1
        return value
    old_scores=copy.deepcopy(scores)
    if isMaxplayer==1:
        pos_value=-2*total
        for i in range(total):
            for j in range(4):
                if j%2==1 or lines[i][j]==1:
                    continue
                x=i//size
                y=i%size
                nx=x+fx[j]
                ny=y+fy[j]
                nVal=nx*size+ny
                corMove=-1
                if j==0:
                    corMove=1
                elif j==1:
                    corMove=0
                elif j==2:
                    corMove=3
                else:
                    corMove=2
                if valid(nx,ny,size)==1:
                    lines[i][j]=1
                    lines[nVal][corMove]=1
                    if gotScore(x,y,lines,scores)==1:
                        # print('before',scores)
                        putScore(x,y,lines,scores,1)
                        # print(scores)
                        pos_value=max(pos_value,minimax(lines,scores,1))
                    else:
                        pos_value=max(pos_value,minimax(lines,scores,0))
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        return pos_value

    else:
        pos_value=2*total
        for i in range(total):
            for j in range(4):
                if j%2==1 or lines[i][j]==1:
                    continue
                x=i//size
                y=i%size
                nx=x+fx[j]
                ny=y+fy[j]
                nVal=nx*size+ny
                corMove=-1
                if j==0:
                    corMove=1
                elif j==1:
                    corMove=0
                elif j==2:
                    corMove=3
                else:
                    corMove=2
                if valid(nx,ny,size)==1:
                    lines[i][j]=1
                    lines[nVal][corMove]=1
                    if gotScore(x,y,lines,scores)==1:
                        putScore(x,y,lines,scores,2)
                        pos_value=min(pos_value,minimax(lines,scores,0))
                    else:
                        pos_value=min(pos_value,minimax(lines,scores,1))
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        return pos_value



def main():



    lines=[[0 for _ in range(4)] for _ in range(total)]
    scores=[[-1 for _ in range(size)] for _ in range(size)]
    Minimax_value=minimax(lines,scores,1)
    print("Number of states: ",count)
    print(Minimax_value)

    

if __name__=="__main__":
    main()