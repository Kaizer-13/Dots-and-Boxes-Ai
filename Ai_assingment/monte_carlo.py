import copy
import math
import random

fx=[1,-1,0,0]
fy=[0,0,1,-1]

cx=[-1,-1,0,0]
cy=[-1,0,-1,0]

sx1=[0,1,0,0]
sy1=[0,0,0,1]
mv=[2,2,0,0]

size=2
total=size*size

count = 0
c=1
n_dic={}
t_dic={}

explored=0

def draw_grid(lines,scores,isMaxplayer):
    if isMaxplayer==1:
        print("First Player: ")
    else:
        print("Second Player: ")
    print("")
    for i in range(size):
        for j in range (size):
            print('*',end='')
            val=i*size+j
            if j+1!=size:
                if lines[val][2]==1:
                    print('-',end='')
                else:
                    print(' ',end='')
        print("")
        if i +1 != size:
            for j in range (size):
                val=i*size+j
                if lines[val][0]==1:
                    print('|',end='')
                    if scores[i][j]!=-1:
                        print(scores[i][j],end='')
                    else:
                        print(' ',end='')
                else:
                    print('  ',end='')
            print("")
    print("")


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

def match_key(key, tuple_key):
    for i in range(3):
        if key[i]!=tuple_key[i]:
            return 0
    return 1


def make_tuple(lines,scores,isMaxplayer):
    global n_dic
    global t_dic
    tuple_of_lines= tuple(tuple(sublist) for sublist in lines)
    tuple_of_scores = tuple(tuple(sublist) for sublist in scores)
    tuple_key = (tuple_of_lines,tuple_of_scores,isMaxplayer)
    for key in n_dic:
        if match_key(key,tuple_key)==1:
            return key
    n_dic[tuple_key]=0
    t_dic[tuple_key]=0
    return tuple_key



def get_UCB1(lines,scores,isMaxplayer,par_isMax):
    global count
    global c
    global n_dic
    global t_dic

    state_tuple=make_tuple(lines,scores,isMaxplayer)
    n_val=0;
    t_val=0;
    n_val=n_dic[state_tuple]
    t_val=t_dic[state_tuple]
    if n_val==0:
        if par_isMax==1:
            return total**10
        else:
            return -total**10
    else:
        val=t_val/n_val
        val=val+c*math.sqrt(math.log(count,2)/n_val)
        return val


def explore(lines, scores, isMaxplayer):
    # draw_grid(lines,scores,isMaxplayer)
    global n_dic
    global t_dic
    global explored
    explored=explored+1

    state_tuple=make_tuple(lines,scores,isMaxplayer)
    
    if isFinish(scores)==1:
        value=0
        for i in range(size-1):
            for j in range(size-1):
                score=scores[i][j]
                if score==2:
                    value=value-1
                elif score==1:
                    value=value+1
        n_dic[state_tuple]=n_dic[state_tuple]+1
        t_dic[state_tuple]=t_dic[state_tuple]+value
        return value
    n_val=n_dic[state_tuple]
    if n_val==0:
        # print(count)
        value=rollout(lines,scores,isMaxplayer,0)
        n_dic[state_tuple]=n_dic[state_tuple]+1
        t_dic[state_tuple]=t_dic[state_tuple]+value
        return value
    old_scores=copy.deepcopy(scores)
    if isMaxplayer==1:
        list_of_moves=[]
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
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),1])
                    else:
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),0])
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        pos_val=-total**10
        nlines=lines
        nscores=scores
        nisMax=isMaxplayer
        for opline,opscore,opisMax in list_of_moves:
            current=get_UCB1(opline,opscore,opisMax,isMaxplayer)
            if current>pos_val:
                nlines=opline
                nscores=opscore
                nisMax=opisMax
                pos_val=current
        value=explore(nlines,nscores,nisMax)
        n_dic[state_tuple]=n_dic[state_tuple]+1
        t_dic[state_tuple]=t_dic[state_tuple]+value
        return value
    else:
        list_of_moves=[]
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
                        putScore(x,y,lines,scores,2)
                        # print(scores)
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),0])
                    else:
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),1])
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        pos_val=total**10
        nlines=lines
        nscores=scores
        nisMax=isMaxplayer
        for opline,opscore,opisMax in list_of_moves:
            current=get_UCB1(opline,opscore,opisMax,isMaxplayer)
            if current<pos_val:
                nlines=opline
                nscores=opscore
                nisMax=opisMax
                pos_val=current
        value=explore(nlines,nscores,nisMax)
        n_dic[state_tuple]=n_dic[state_tuple]+1
        t_dic[state_tuple]=t_dic[state_tuple]+value
        return value


def rollout(lines, scores, isMaxplayer, draw):
    if draw==1:
        draw_grid(lines,scores,isMaxplayer)
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
        list_of_moves=[]
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
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),1])
                    else:
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),0])
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        options=len(list_of_moves)
        pos_val=random.randint(0, options-1)
        opline,opscore,opisMax=list_of_moves[pos_val]
        return rollout(opline,opscore,opisMax,draw)
    else:
        list_of_moves=[]
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
                        putScore(x,y,lines,scores,2)
                        # print(scores)
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),0])
                    else:
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),1])
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        options=len(list_of_moves)
        pos_val=random.randint(0, options-1)
        opline,opscore,opisMax=list_of_moves[pos_val]
        return rollout(opline,opscore,opisMax,draw)

def simulate(lines,scores, isMaxplayer):
    if isFinish(scores)==1:
        return
    old_scores=copy.deepcopy(scores)
    if isMaxplayer==1:
        list_of_moves=[]
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
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),1])
                    else:
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),0])
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        pos_val=-total**10
        nlines=lines
        nscores=scores
        nisMax=isMaxplayer
        for opline,opscore,opisMax in list_of_moves:
            current=get_UCB1(opline,opscore,opisMax,isMaxplayer)
            if current>pos_val and abs(current)!=(total**10):
                nlines=opline
                nscores=opscore
                nisMax=opisMax
                pos_val=current
        if pos_val<total:
            rollout(nlines,nscores,nisMax,1)
        else:
            draw_grid(lines,scores,isMaxplayer)
            simulate(nlines,nscores,nisMax)
    else:
        list_of_moves=[]
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
                        putScore(x,y,lines,scores,2)
                        # print(scores)
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),0])
                    else:
                        list_of_moves.append([copy.deepcopy(lines),copy.deepcopy(scores),1])
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        pos_val=total**10
        nlines=lines
        nscores=scores
        nisMax=isMaxplayer
        for opline,opscore,opisMax in list_of_moves:
            current=get_UCB1(opline,opscore,opisMax,isMaxplayer)
            if current<pos_val and abs(current)!=(total**10):
                nlines=opline
                nscores=opscore
                nisMax=opisMax
                pos_val=current
        if pos_val>total:
            rollout(nlines,nscores,nisMax,0)
        else:
            draw_grid(lines,scores,isMaxplayer)
            simulate(nlines,nscores,nisMax)


def main():
    global size
    global total
    size =int(input("Enter the dimensons of the grid: "))
    limit = int(input("Enter the number of cycles for exploration: "))
    total=size*size

    
    global count
    count=0
    while count < limit:
        lines=[[0 for _ in range(4)] for _ in range(total)]
        scores=[[-1 for _ in range(size)] for _ in range(size)]
        explore(lines,scores,1)
        count=count+1


    print("Number of states explored: ",explored)
    lines=[[0 for _ in range(4)] for _ in range(total)]
    scores=[[-1 for _ in range(size)] for _ in range(size)]
    print("UCB1 Value at root:",get_UCB1(lines,scores,1,0))
    draw_grid(lines,scores,1)
    simulate(lines,scores,1)

if __name__=="__main__":
    main()