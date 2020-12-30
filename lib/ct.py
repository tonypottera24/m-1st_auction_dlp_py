from lib.big_number import BigNumber
from random import randrange
from lib.same_dl_proof import SameDLProof
from constants.dlp import DLP


class Ct():
    def __init__(self, u, c):
        self.u, self.c = u, c

    @classmethod
    def from_sol(cls, a):
        u = [BigNumber.from_sol(u).to_py() for u in a[0]]
        c = BigNumber.from_sol(a[1]).to_py()
        return cls(u, c)

    @classmethod
    def from_plaintext(cls, m, y):
        r = [randrange(1, DLP.q) for yy in y]
        u = [pow(DLP.g, rr, DLP.p) for rr in r]
        c = m % DLP.p
        for yy, rr in zip(y, r):
            c = (c * pow(yy, rr, DLP.p)) % DLP.p
        return cls(u, c)

    def decrypt(self, index, x):
        u = self.u[index]
        assert(0 < u and u < DLP.p)
        assert(0 < x and x < DLP.q)
        ux = pow(u, x, DLP.p)
        ux_inv = pow(ux, -1, DLP.p)
        assert((ux * ux_inv) % DLP.p == 1)
        pi = SameDLProof(u, DLP.g, x)
        return ux, ux_inv, pi

    def decrypt_to_sol(self, index, x):
        ux, ux_inv, pi = self.decrypt(index, x)
        return BigNumber.from_py(ux).to_sol(), BigNumber.from_py(ux_inv).to_sol(), pi.to_sol()

    def mul_z(self, z):
        assert(z > 0)
        return Ct(self.u, (self.c * z) % DLP.p)

    def pow(self, k):
        assert(k > 0)
        u = [pow(uu, k, DLP.p) for uu in self.u]
        c = pow(self.c, k, DLP.p)
        return Ct(u, c)

    def to_sol(self):
        u = [BigNumber.from_py(uu).to_sol() for uu in self.u]
        c = BigNumber.from_py(self.c).to_sol()
        return u, c
