from lib.big_number import BigNumber
from random import randrange
from lib.same_dl_proof import SameDLProof
from constants.dlp import DLP


class Ct():
    def __init__(self, u: int, c: int):
        self.u, self.c = u, c

    @classmethod
    def from_sol(cls, a: list):
        u = BigNumber.from_sol(a[0]).to_py()
        c = BigNumber.from_sol(a[1]).to_py()
        return cls(u, c)

    @classmethod
    def from_plaintext(cls, m: int, y: list):
        r = randrange(1, DLP.q)
        u = pow(DLP.g, r, DLP.p)
        c = m % DLP.p
        for yy in y:
            c = (c * pow(yy, r, DLP.p)) % DLP.p
        return cls(u, c)

    def decrypt(self, x: int):
        assert(0 < self.u and self.u < DLP.p)
        assert(0 < x and x < DLP.q)
        ux = pow(self.u, x, DLP.p)
        ux_inv = pow(ux, -1, DLP.p)
        assert((ux * ux_inv) % DLP.p == 1)
        pi = SameDLProof(self.u, DLP.g, x)
        return ux, ux_inv, pi

    def decrypt_to_sol(self, x: int):
        ux, ux_inv, pi = self.decrypt(x)
        return BigNumber.from_py(ux).to_sol(), BigNumber.from_py(ux_inv).to_sol(), pi.to_sol()

    def mul_z(self, z: int):
        assert(z > 0)
        return Ct(self.u, (self.c * z) % DLP.p)

    def pow(self, k: int):
        assert(k > 0)
        u = pow(self.u, k, DLP.p)
        c = pow(self.c, k, DLP.p)
        return Ct(u, c)

    def to_sol(self):
        u = BigNumber.from_py(self.u).to_sol()
        c = BigNumber.from_py(self.c).to_sol()
        return u, c
