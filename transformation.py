from numpy import *
import binascii


def BinStr2Int(s):
    return int(s, 0b10)


def Int2BinStr(num, n=32):
    s = bin(num)[2:]
    if n >= len(s):
        s = '0' * (n - len(s)) + s
        return s
    else:
        return s


def Int2HexStr(num, n=8):
    s = hex(num)
    if s[-1] == 'L':
        s = s[2:-1]
    else:
        s = s[2:]
    if n >= len(s):
        s = '0' * (n - len(s)) + s
        return s
    else:
        return s


def HexStr2Int(s):
    return int(s, 0x10)


def HexStr2BinList(s, n=32):
    l = list(Int2BinStr(HexStr2Int(s), n))
    for i in xrange(len(l)):
        l[i] = ord(l[i]) - ord('0')
    return l


def BinList2HexStr(l):
    for i in xrange(len(l)):
        l[i] = str(l[i])
    l = ''.join(l)
    return Int2HexStr(BinStr2Int(l), len(l) / 4)


def BinList2BinArray(l):
    return array(l)


def BinArray2BinList(a):
    l = ndarray.tolist(a)
    for i in xrange(len(l)):
        l[i] = int(l[i])
    return l
