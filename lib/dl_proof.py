from random import randrange
from web3 import Web3
from lib.big_number import BigNumber
from constants.dlp import DLP1024


class DLProof():
    def __init__(self, g, x):
        y = pow(g, x, DLP1024.p)
        v = randrange(1, DLP1024.q)
        t = pow(g, v, DLP1024.p)
        c = Web3.solidityKeccak(['bytes'], [
            BigNumber.from_py(g).val + BigNumber.from_py(y).val + BigNumber.from_py(t).val])
        c = int.from_bytes(c, byteorder='big') % DLP1024.q
        r = (v - (c * x) % DLP1024.q) % DLP1024.q
        if r < 0:
            r += DLP1024.q
        assert(t == (pow(g, r, DLP1024.p) * pow(y, c, DLP1024.p)) % DLP1024.p)
        self.t, self.r = t, r

    def to_sol(self):
        return BigNumber.from_py(self.t).to_sol(), BigNumber.from_py(self.r).to_sol()
