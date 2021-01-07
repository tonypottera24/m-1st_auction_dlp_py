from lib.ct_01_proof import Ct01Proof
from lib.big_number import BigNumber
from random import randrange
from lib.same_dl_proof import SameDLProof
from constants.dlp import DLP


class Ct():
    def __init__(self, u, c, r=None, ct_01_proof=None):
        self.u, self.c = u, c
        self.r = r
        self.ct_01_proof = ct_01_proof

    @classmethod
    def from_sol(cls, a):
        u = BigNumber.from_sol(a[0]).to_py()
        c = BigNumber.from_sol(a[1]).to_py()
        return cls(u, c)

    @classmethod
    def from_vote(cls, v, y):
        r = randrange(1, DLP.q)
        u = pow(DLP.g, r, DLP.p)
        zt = pow(DLP.z, 1 if v else 0, DLP.p)
        c = zt * pow(y, r, DLP.p) % DLP.p
        return cls(u, c, r=r, ct_01_proof=Ct01Proof(v, u, c, r, y))

    def decrypt(self, x):
        assert(0 < self.u and self.u < DLP.p)
        assert(0 < x and x < DLP.q)
        ux = pow(self.u, x, DLP.p)
        ux_inv = pow(ux, -1, DLP.p)
        assert((ux * ux_inv) % DLP.p == 1)
        pi = SameDLProof(self.u, DLP.g, x)
        return ux, ux_inv, pi

    def decrypt_to_sol(self, x):
        ux, ux_inv, pi = self.decrypt(x)
        return BigNumber.from_py(ux).to_sol(), BigNumber.from_py(ux_inv).to_sol(), pi.to_sol()

    def mul(self, ct):
        return Ct(self.u * ct.u % DLP.p, self.c * ct.c % DLP.p, r=(self.r + ct.r) % DLP.q)

    def mul_z(self, z):
        assert(z > 0)
        return Ct(self.u, self.c * z % DLP.p)

    def pow(self, k):
        assert(k > 0)
        u = pow(self.u, k, DLP.p)
        c = pow(self.c, k, DLP.p)
        return Ct(u, c, r=(self.r+k) % DLP.q if self.r != None else None)

    def to_sol(self):
        return BigNumber.from_py(self.u).to_sol(), BigNumber.from_py(self.c).to_sol()

    def to_sol_with_01_proof(self):
        return self.to_sol(), self.ct_01_proof.to_sol()
