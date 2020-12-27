from random import randrange
from web3 import Web3
from lib.big_number import BigNumber
from constants.dlp import DLP1024


class SameDLProof():
    def __init__(self, g1, g2, x):
        y1, y2 = pow(g1, x, DLP1024.p), pow(g2, x, DLP1024.p)
        v = randrange(1, DLP1024.q)
        t1, t2 = pow(g1, v, DLP1024.p), pow(g2, v, DLP1024.p)
        c = Web3.solidityKeccak(['bytes'], [
                                BigNumber.from_py(g1).val + BigNumber.from_py(g2).val + BigNumber.from_py(y1).val + BigNumber.from_py(y2).val + BigNumber.from_py(t1).val + BigNumber.from_py(t2).val])
        c = int.from_bytes(c, byteorder='big') % DLP1024.q
        r = (v - (c * x) % DLP1024.q) % DLP1024.q
        if r < 0:
            r += DLP1024.q
        assert(c > 0 and r > 0)
        assert(t1 == (pow(g1, r, DLP1024.p) * pow(y1, c, DLP1024.p)) % DLP1024.p)
        assert(t2 == (pow(g2, r, DLP1024.p) * pow(y2, c, DLP1024.p)) % DLP1024.p)
        self.t1, self.t2, self.r = t1, t2, r

    def to_sol(self):
        return BigNumber.from_py(self.t1).to_sol(), BigNumber.from_py(self.t2).to_sol(), BigNumber.from_py(self.r).to_sol()
