# coding=utf-8
# Author: Lyy
# Email: henryly94@gmail.com
import binascii
import binmatrix as bm
import transformation as tr
import encrypt as en
import datetime as time

rk = [0xf12186f9, 0x41662b61, 0x5a6ab19a, 0x7ba92077,
      0x367360f4, 0x776a0c61, 0xb6bb89b3, 0x24763151,
      0xa520307c, 0xb7584dbd, 0xc30753ed, 0x7ee55b57,
      0x6988608c, 0x30d895b7, 0x44ba14af, 0x104495a1,
      0xd120b428, 0x73b55fa3, 0xcc874966, 0x92244439,
      0xe89e641f, 0x98ca015a, 0xc7159060, 0x99e1fd2e,
      0xb79bd80c, 0x1d2115b0, 0x0e228aeb, 0xf1780c81,
      0x428d3654, 0x62293496, 0x01cf72e5, 0x9124a012]

A = []
for i in xrange(32):
    A.append([])
    for j in xrange(4):
        A[i].append(bm.gen(32, 32))

b = []
for i in xrange(32):
    b.append([])
    for j in xrange(4):
        b[i].append(bm.gen(1, 32))

line = 128 / 8  # len of string is 16(128 bits)

rest = '#'

trans = lambda s: binascii.b2a_hex(s)

inverse = lambda h: binascii.a2b_hex(h)

xor = lambda a, b: tr.Int2HexStr(tr.HexStr2Int(a) ^ tr.HexStr2Int(b), len(a))


def split_pt(pt):
    for i in xrange(0, len(pt), line):
        yield (pt[i:i+line] + rest * line)[:line]


def A_1(x):
    global r
    x = tr.BinList2BinArray(tr.HexStr2BinList(x))
    return xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(x, A[r][0]))),
               tr.BinList2HexStr(tr.BinArray2BinList(b[r][0])))


def A_2(x):
    global r
    x = tr.BinList2BinArray(tr.HexStr2BinList(x))
    return xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(x, A[r][1]))),
               tr.BinList2HexStr(tr.BinArray2BinList(b[r][1])))


def A_3(x):
    global r
    x = tr.BinList2BinArray(tr.HexStr2BinList(x))
    return xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(x, A[r][2]))),
               tr.BinList2HexStr(tr.BinArray2BinList(b[r][2])))


def A_4(x):
    global r
    x = tr.BinList2BinArray(tr.HexStr2BinList(x))
    return xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(x, A[r][3]))),
               tr.BinList2HexStr(tr.BinArray2BinList(b[r][3])))


def func_A(x, param):
    # This function is corresponding to transformation A_{r,param}, or A^{-1}_{r,param} when param < 0
    func_map = {
        1: A_1,
        2: A_2,
        3: A_3,
        4: A_4
    }
    return func_map[abs(param)](x)


def U_r(x):
    return xor(en.L(x[0:8]), en.R(x[9:16]))


def EP_r(rk_r):
    WK_r = []
    EP = bm.gen(32, 64)
    rk_r = tr.BinList2BinArray(tr.HexStr2BinList(tr.Int2HexStr(rk_r)))
    WK = tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(rk_r, EP)))
    for i in xrange(0, len(WK), 2):
        WK_r.append(WK[i] + WK[i + 1])
    return WK_r


def T_r(x):
    global r
    WK_r = EP_r(rk[r])
    s = ''
    for i in xrange(0, len(x), 2):
        s += en.Sbox(xor((x[i] + x[i + 1]), WK_r[i / 2]))
    return s


def E_r(x):
    s = ''
    for i in xrange(len(x)):
        A = bm.gen(4, 8)
        b = bm.gen(1, 8)
        x_i = tr.BinList2BinArray(tr.HexStr2BinList(x[i], 4))
        y_i = xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(x_i, A))), tr.BinList2HexStr(tr.BinArray2BinList(b)))
        s += y_i
    return s


def get_y(x):
    s = U_r(T_r(E_r(x)))
    return s



def wb_crypt(plain_text):
    # main function, take string as input and return encrypted text,
    global r

    text = split_pt(plain_text)

    cipher_text = ''

    for each in text:
        x = [trans(each[i:i+line/4]) for i in xrange(0, line, line/4)]
        print 'Plain text block: ' + ''.join(x)
        print 'Encryption start: '
        print 'Pre-procession start: '

        x[0] = xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(tr.BinList2BinArray(tr.HexStr2BinList(x[0])), bm.inv(A[0][2])))),
                   tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(b[0][2], bm.inv(A[0][2])))))
        x[1] = xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(tr.BinList2BinArray(tr.HexStr2BinList(x[1])), bm.inv(A[0][0])))),
                   tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(b[0][0], bm.inv(A[0][0])))))
        x[2] = xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(tr.BinList2BinArray(tr.HexStr2BinList(x[2])), bm.inv(A[0][0])))),
                   tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(b[0][0], bm.inv(A[0][0])))))
        x[3] = xor(tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(tr.BinList2BinArray(tr.HexStr2BinList(x[3])), bm.inv(A[0][0])))),
                   tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(b[0][0], bm.inv(A[0][0])))))
        print 'Pre-processed text block: ' + ''.join(x)

        for i in xrange(32):
            # X^{r} = O_r (x_{r,1} ^ x_{r,2} ^ x_{r,3})
            X_r = func_A(func_A(xor(xor(x[1], x[2]), x[3]), -1), 4)
            # print 'X_r: ' + X_r

            # X_{r,0} = P_r (x_{r,0})
            X_r_0 = func_A(func_A(x[0], -3), 4)
            # print 'X_r_0: ' + X_r_0

            # get y_{r,1}... y_{r,8}
            y = list(get_y(X_r))
            # print 'y: ' + str(y)

            new_x = reduce(xor, y, X_r_0)
            x = x[1:] + [new_x]

            print 'Round ' + str(i) + ': ' + ''.join(x)

            r = r + 1

        # Accumulate (x_{31,3}, x_{31,2}, x_{31,1}, x_{31,0})
        cipher_text += reduce(lambda a, b: a+b, map(inverse, x[-1::-1]))
        r = 0
        print '----------------------------------------------------------------------'
    print 'Cipher text: '
    print cipher_text


if __name__ == '__main__':
    global r
    r = 0

    start = time.datetime.now()
    wb_crypt('abcdefghijklmnopqrstuvwxyza')
    end = time.datetime.now()
    print 'Total time: '
    print end - start