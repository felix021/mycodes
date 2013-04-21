class RSEncoder(object):
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.q = n + 1

        G.<a> = GF(self.q)
        alphas = [a^i for i in range(n)]

        #calculate map and reverse map from GF(8) to integers
        Gmap  = {}
        Gmapr = {}
        for i in range(self.q):
            binary = map(int, bin(i)[2:])
            binary.reverse()
            alpha = G(binary)
            Gmap[i] = alpha
            Gmapr[alpha] = i

        #P: univariable polynomial class over G
        P = G['x']

        self.G = G
        self.a = a
        self.alphas = alphas
        self.Gmap = Gmap
        self.Gmapr = Gmapr
        self.P = P

    def encode(self, msg):
        Pmsg = self.P([self.Gmap[i] for i in msg])
        return [self.Gmapr[Pmsg(i)] for i in self.alphas]

rs = RSEncoder(63, 4)

for i in range(1<<8):
    uid = []
    for j in range(4):
        uid.append((i % 64))
        i = i // 64
    uid.reverse()
    print rs.encode(uid)
