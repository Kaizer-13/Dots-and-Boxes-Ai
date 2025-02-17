
n=int(input("Enter Dimention of points: "))
ops=2*n*(n-1)
value=0
curr=1
nxt=ops
for i in range(ops+1):
    value=value+curr
    curr=curr*nxt
    nxt=nxt-1

print("Number of possible states in search space: ",value)