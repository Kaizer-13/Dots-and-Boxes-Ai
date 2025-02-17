import copy
fx=[1,-1,0,0]
fy=[0,0,1,-1]

cx=[-1,-1,0,0]
cy=[-1,0,-1,0]

sx1=[0,1,0,0]
sy1=[0,0,0,1]
mv=[2,2,0,0]

size=3
total=size*size

def draw_grid(lines,scores):
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


def minimax(lines, scores, isMaxplayer,alpha,beta):
    # draw_grid(lines,scores)
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
                        putScore(x,y,lines,scores,1)
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=max(pos_value,minimax(lines,scores,1,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        alpha=max(alpha,pos_value)
                        if beta <= alpha:
                            lines[i][j]=0
                            lines[nVal][corMove]=0
                            scores=copy.deepcopy(old_scores)
                            return pos_value
                    else:
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=max(pos_value,minimax(lines,scores,0,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        alpha=max(alpha,pos_value)
                        if beta <= alpha:
                            lines[i][j]=0
                            lines[nVal][corMove]=0
                            scores=copy.deepcopy(old_scores)
                            return pos_value
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
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=min(pos_value,minimax(lines,scores,0,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        beta=min(beta,pos_value)
                        if beta <= alpha:
                            lines[i][j]=0
                            lines[nVal][corMove]=0
                            scores=copy.deepcopy(old_scores)
                            return pos_value
                    else:
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=min(pos_value,minimax(lines,scores,1,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        beta=min(beta,pos_value)
                        if beta <= alpha:
                            lines[i][j]=0
                            lines[nVal][corMove]=0
                            scores=copy.deepcopy(old_scores)
                            return pos_value
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)
        return pos_value

def print_game(lines, scores, isMaxplayer,alpha,beta,Minimax_value):
    draw_grid(lines,scores)
    if isFinish(scores)==1:
        return
    old_scores=copy.deepcopy(scores)
    if isMaxplayer==1:
        print("First Player:")
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
                        putScore(x,y,lines,scores,1)
                        this_score=copy.deepcopy(scores)
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=max(pos_value,minimax(lines,scores,1,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        if pos_value==Minimax_value:
                            print_game(lines,this_score,1,alpha,beta,Minimax_value)
                            return
                        alpha=max(alpha,pos_value)
                    else:
                        old_alpha=alpha
                        old_beta=beta
                        this_score=copy.deepcopy(scores)
                        pos_value=max(pos_value,minimax(lines,scores,0,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        if pos_value==Minimax_value:
                            print_game(lines,this_score,0,alpha,beta,Minimax_value)
                            return
                        alpha=max(alpha,pos_value)
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)

    else:
        print("Second Player:")
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
                        this_score=copy.deepcopy(scores)
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=min(pos_value,minimax(lines,scores,0,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        if pos_value==Minimax_value:
                            print_game(lines,this_score,0,alpha,beta,Minimax_value)
                            return
                        beta=min(beta,pos_value)
                    else:
                        this_score=copy.deepcopy(scores)
                        old_alpha=alpha
                        old_beta=beta
                        pos_value=min(pos_value,minimax(lines,scores,1,alpha,beta))
                        alpha=old_alpha
                        beta=old_beta
                        if pos_value==Minimax_value:
                            print_game(lines,this_score,1,alpha,beta,Minimax_value)
                            return
                        beta=min(beta,pos_value)
                    lines[i][j]=0
                    lines[nVal][corMove]=0
                    scores=copy.deepcopy(old_scores)

def main():
    global size
    global total
    size =int(input("Enter the dimensons of the grid: "))
    total=size*size
    lines=[[0 for _ in range(4)] for _ in range(total)]
    scores=[[-1 for _ in range(size)] for _ in range(size)]
    alpha=-2*total-50000
    beta=2*total+50000
    Minimax_value=minimax(lines,scores,1,alpha,beta)
    print("Number of states: ",count)
    print(Minimax_value)
    lines=[[0 for _ in range(4)] for _ in range(total)]
    scores=[[-1 for _ in range(size)] for _ in range(size)]
    print_game(lines,scores,1,-2*total-50000,2*total+50000,Minimax_value)

if __name__=="__main__":
    main()