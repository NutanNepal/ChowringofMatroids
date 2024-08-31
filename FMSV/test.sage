def reduced_char_poly(M):
    return char_poly(M) // (x - 1)

def char_poly(M):
    T = M.tutte_polynomial()
    x = var('x')
    subbed_Tpoly = T.subs(x = 1 - x, y = 0)
    char_poly = (-1) ** M.rank() * subbed_Tpoly
    R = PolynomialRing(QQ, 'x')

    return R(char_poly)

l = [(i,j) for i in range(1, 10) for j in range(1, i+1)]

for i, j in l:
    M = matroids.Uniform(j, i)
    cp = char_poly(M)
    print("U(",j,i, ")", cp, ",", cp//(x-1))
