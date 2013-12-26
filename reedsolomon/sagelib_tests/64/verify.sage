import sagelib

n = 63
k = 4
q = n + 1

G.<a> = GF(q)
alphas = [a^i for i in range(n)]
Gmap  = {}
Gmapr = {}
for i in range(q):
    binary = map(int, bin(i)[2:])
    binary.reverse()
    alpha = G(binary)
    Gmap[i] = alpha
    Gmapr[alpha] = i
P = G['x']

#cw = [0, 27, 46, 7, 35, 52, 58, 17, 37, 4, 59, 25, 62, 49, 18, 61, 41, 63, 57, 9, 8, 0, 27, 46, 7, 35, 52, 58, 17, 37, 4, 59, 25, 62, 49, 18, 61, 41, 63, 57, 9, 8, 0, 27, 46, 7, 35, 52, 58, 17, 37, 4, 59, 25, 62, 49, 18, 61, 41, 63, 57, 9, 8]

for line in open("uids.txt"):
    nums = map(int, line.strip().split())
    uid = nums[0]
    cw = nums[1:]
    print uid

    codeword = [Gmap[i] for i in cw]

    points = zip(alphas, codeword, [2] * n)
    Cost = sum([m * (m + 1) / 2 for x,y,m in points])

    weight_y = k - 1

    max_deg_y = floor((1 + sqrt(1 + 8 * Cost / weight_y)) / 2) - 1
    Q = sagelib.kv.gs_construct_Q(points, max_deg_y, weight_y)

    Pmsg_list = sagelib.factor_bivariate_linear(Q, weight_y)

    decode_ok = False
    for p in Pmsg_list:
        m = map(lambda x: Gmapr[x], p)
        #zero padding at the rear end
        msg = m + [0] * (k - len(m))
        duid = msg[0] * 64**3 + msg[1] * 64 ** 2 + msg[2] * 64 + msg[3]
        print msg, duid, uid
        if duid == uid:
            decode_ok = True
            print 'decode ok'
    if decode_ok:
        print uid
    else:
        print nums
        break
