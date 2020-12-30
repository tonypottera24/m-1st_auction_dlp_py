from random import randrange
from web3 import Web3
from lib.big_number import BigNumber
from constants.dlp import DLP


class DLProof():
    def __init__(self, g, x):
        y = pow(g, x, DLP.p)
        v = randrange(1, DLP.q)
        t = pow(g, v, DLP.p)
        c = Web3.solidityKeccak(['bytes'], [
            BigNumber.from_py(g).val + BigNumber.from_py(y).val + BigNumber.from_py(t).val])
        c = int.from_bytes(c, byteorder='big') % DLP.q
        r = (v - (c * x) % DLP.q) % DLP.q
        assert(t == (pow(g, r, DLP.p) * pow(y, c, DLP.p)) % DLP.p)
        self.t, self.r = t, r

    def to_sol(self):
        return BigNumber.from_py(self.t).to_sol(), BigNumber.from_py(self.r).to_sol()
