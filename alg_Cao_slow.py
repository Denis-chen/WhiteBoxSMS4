from numpy import *
import binascii
import transformation as tr
import binmatrix as bm
import datetime as time

SboxTable = [
    [0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05],
    [0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99],
    [0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62],
    [0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6],
    [0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8],
    [0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35],
    [0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87],
    [0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e],
    [0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1],
    [0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3],
    [0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f],
    [0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51],
    [0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8],
    [0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0],
    [0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84],
    [0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]
]

rk = [0xf12186f9, 0x41662b61, 0x5a6ab19a, 0x7ba92077,
      0x367360f4, 0x776a0c61, 0xb6bb89b3, 0x24763151,
      0xa520307c, 0xb7584dbd, 0xc30753ed, 0x7ee55b57,
      0x6988608c, 0x30d895b7, 0x44ba14af, 0x104495a1,
      0xd120b428, 0x73b55fa3, 0xcc874966, 0x92244439,
      0xe89e641f, 0x98ca015a, 0xc7159060, 0x99e1fd2e,
      0xb79bd80c, 0x1d2115b0, 0x0e228aeb, 0xf1780c81,
      0x428d3654, 0x62293496, 0x01cf72e5, 0x9124a012]

BLOCK_SIZE = 128 / 8

trans = lambda s: binascii.b2a_hex(s)

inverse = lambda h: binascii.a2b_hex(h)

xor = lambda a, b: tr.Int2HexStr(tr.HexStr2Int(a) ^ tr.HexStr2Int(b), len(a))


def split_pt(pt, blk_size):
    for i in xrange(0, len(pt), blk_size):
        yield (pt[i:i + blk_size] + '#' * blk_size)[:blk_size]


def nonlinear(table, m, n, bij = False):
    if m == n and bij:
        used = []
        for i in xrange(2 ** n):
            used.append(False)

        for i in xrange(2 ** m):
            value = random.randint(0, 2 ** n)
            while used[value]:
                value = random.randint(0, 2 ** n)
            table.append(value)
            used[value] = True
    else:
        for i in xrange(2 ** m):
            value = random.randint(0, 2 ** n)
            table.append(value)


def TCon(Tbox):
    for r in xrange(32):
        Tbox.append([])
        WK = []
        for i in xrange(4):
            Tbox[r].append([])
            Tbox[r][2*i] = []
            Tbox[r].append([])
            Tbox[r][2*i+1] = []

            EP = []
            nonlinear(EP, 8, 16)
            WK.append(EP[(rk[r] % (2 ** (32 - 8 * i))) / (2 ** (24 - 8 * i))])
            for n in xrange(2 ** 8):
                v1 = (WK[i] / 2 ** 8) ^ n
                v2 = (WK[i] % 2 ** 8) ^ n
                Tbox[r][2 * i].append(SboxTable[v1 / 16][v1 % 16])
                Tbox[r][2 * i + 1].append(SboxTable[v2 / 16][v2 % 16])


def UCon(U):
    LR = hstack((random.randint(0, 1, (32, 32)), random.randint(0, 2, (32, 32))))
    for i in xrange(32):
        LR[i][i] ^= 1
        LR[i][(i + 2) % 32] ^= 1
        LR[i][(i + 10) % 32] ^= 1
        LR[i][(i + 18) % 32] ^= 1
        LR[i][(i + 24) % 32] ^= 1
    for r in xrange(32):
        U.append([])
        P = random.randint(0, 1, (64, 64))
        level = 6
        PM = []
        nonlinear(PM, level, level)
        for i in xrange(2 ** level):
            k = PM[i]
            for j in xrange(64 / (2 ** level)):
                P[(64 / (2 ** level)) * k + j][(64 / (2 ** level)) * i + j] ^= 1
        M = hsplit(dot(LR, P) % 2, 8)
        for i in xrange(8):
            U[r].append([])
            for n in xrange(2 ** 8):
                U[r][i].append(dot(M[i], tr.BinList2BinArray(tr.HexStr2BinList(tr.Int2HexStr(n, 2), 8))) % 2)


def LUTCon(LUTable):
    for r in xrange(32):
        LUTable.append([])
        for i in xrange(8):
            LUTable[r].append([])
            LUTable[r][i] = []
            nonlinear(LUTable[r][i], 4, 8)
            for n in xrange(2 ** 4):
                LUTable[r][i][n] = Tbox[r][i][LUTable[r][i][n]]
                LUTable[r][i][n] = U[r][i][LUTable[r][i][n]]


def or_constructor(or_table):
    for r in xrange(32):
        or_table.append([])
        for i in xrange(8):
            or_table[r].append([])
            or_table[r][i] = []
            nonlinear(or_table[r][i], 4, 4, True)


def pr_constructor(pr_table):
    for r in xrange(32):
        pr_table.append([])
        pr_table[r].append([])
        pr_table[r].append([])
        pr_table[r][0] = bm.gen(32, 32)
        pr_table[r][1] = bm.gen(1, 32)



table_gen_start = time.datetime.now()

# global Tbox
Tbox = []
TCon(Tbox)

# global U
U = []
UCon(U)

# global LUTable
LUTable = []
LUTCon(LUTable)

# global or_table
or_table = []
or_constructor(or_table)

table_gen_end = time.datetime.now()

# global pr_table
pr_table = []
pr_constructor(pr_table)


def wb_crypt(pt):

    text = split_pt(pt, BLOCK_SIZE)

    cipher_text = 'ct: '
    plain_text = 'pt: '

    for each in text:
        # each: 128 bit
        x = [trans(each[i:i + BLOCK_SIZE / 4]) for i in xrange(0, BLOCK_SIZE, BLOCK_SIZE / 4)]
        # x[i]: '61626364' -> 'abcd'
        print 'Plain text block: ' + ''.join(x)
        print 'Encryption start.'
        for r in xrange(32):
            X_r = xor(xor(x[1], x[2]), x[3])
            for i in xrange(8):
                X_r = X_r[0:i] + tr.Int2HexStr(or_table[r][i][tr.HexStr2Int(X_r[i])], 1) + X_r[i + 1:]

            # X_r_0 = x[0]
            X_r_0 = xor(tr.BinList2HexStr(
                tr.BinArray2BinList(bm.mlti(pr_table[r][0], tr.BinList2BinArray(tr.HexStr2BinList(x[0]))))),
                tr.BinList2HexStr(tr.BinArray2BinList(pr_table[r][1])))

            y = '00000000'
            for i in xrange(8):
                y = xor(tr.BinList2HexStr(tr.BinArray2BinList(LUTable[r][i][tr.HexStr2Int(X_r[i])])), y)

            new_x = xor(X_r_0, y)
            new_x = xor(
                tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(bm.inv(pr_table[r][0]), pr_table[r][1]))),
                tr.BinList2HexStr(tr.BinArray2BinList(
                    bm.mlti(bm.inv(pr_table[r][0]), tr.BinList2BinArray(tr.HexStr2BinList(new_x))))))
            x = x[1:] + [new_x]

            print 'Round ' + str(r) + ': ' + ''.join(x)

        cipher_text += reduce(lambda a, b: a + b, map(inverse, x[-1::-1]))

        x = [x[3], x[2], x[1], x[0]]
        print 'Cipher text block: ' + ''.join(x)
        print 'Decryption start.'
        for r in xrange(32):
            X_r = xor(xor(x[1], x[2]), x[3])
            for i in xrange(8):
                X_r = X_r[0:i] + tr.Int2HexStr(or_table[31 - r][i][tr.HexStr2Int(X_r[i])], 1) + X_r[i + 1:]

            # X_r_0 = x[0]
            X_r_0 = xor(tr.BinList2HexStr(
                tr.BinArray2BinList(bm.mlti(pr_table[31 - r][0], tr.BinList2BinArray(tr.HexStr2BinList(x[0]))))),
                tr.BinList2HexStr(tr.BinArray2BinList(pr_table[31 - r][1])))

            y = '00000000'
            for i in xrange(8):
                y = xor(tr.BinList2HexStr(tr.BinArray2BinList(LUTable[31 - r][i][tr.HexStr2Int(X_r[i])])), y)

            new_x = xor(X_r_0, y)
            new_x = xor(
                tr.BinList2HexStr(tr.BinArray2BinList(bm.mlti(bm.inv(pr_table[31 - r][0]), pr_table[31 - r][1]))),
                tr.BinList2HexStr(tr.BinArray2BinList(
                    bm.mlti(bm.inv(pr_table[31 - r][0]), tr.BinList2BinArray(tr.HexStr2BinList(new_x))))))
            x = x[1:] + [new_x]
            print 'Round ' + str(r) + ': ' + ''.join(x)
        print '----------------------------------------------------------------------'

        plain_text += reduce(lambda a, b: a + b, map(inverse, x[-1::-1]))

    print plain_text
    print cipher_text


if __name__ == '__main__':

    start = time.datetime.now()
    wb_crypt('abcdefghijklmnopqrstuvwxyzd')
    end = time.datetime.now()
    print 'Table generation: '
    print table_gen_end - table_gen_start
    print 'Total time: '
    print end - start