from numpy import *
import binascii
import transformation as tr


def gen(n, m):
    a = random.randint(0, 2, size=[n, m])
    if n == m:
        while True:
            a = random.randint(0, 2, size=[n, n])
            if linalg.matrix_rank(a) == n and linalg.det(a) % 2 == 1:
                break
    if n == 1:
        a = a[0]
    return a


def alg_minor(matrix, i, j):
    l = len(matrix)
    minor = zeros((l-1, l-1), dtype=int32)
    for m in xrange(l):
        for n in xrange(l):
            if (m < i) and (n < j):
                minor[m][n] = matrix[m][n]
            elif (m < i) and (n > j):
                minor[m][n - 1] = matrix[m][n]
            elif (m > i) and (n < j):
                minor[m - 1][n] = matrix[m][n]
            elif (m > i) and (n > j):
                minor[m - 1][n - 1] = matrix[m][n]
    return minor


def mlti(s, t):
    return dot(s, t) % 2


def inv(matrix):
    n = len(matrix)
    inv = zeros((n, n), dtype=int32)
    for i in xrange(n):
        for j in xrange(n):
            inv[i][j] = int(round(linalg.det(alg_minor(matrix, j, i)))) % 2
            # int(linalg.det((alg_minor(matrix, j, i))) % 2)
    return inv
