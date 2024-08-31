l = [(i,j) for i in range(1, 10) for j in range(1, i+1)]

for i, j in l:
    print("U(",j,i, ")")