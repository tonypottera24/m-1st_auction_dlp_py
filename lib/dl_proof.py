from random import randrange
from web3 import Web3
from lib.big_number import BigNumber
from constants.dlp import DLP


class DLProof():
    def __init__(self, g, x):
        y = pow(g, x, DLP.p)
        rr = randrange(1, DLP.q)
        grr = pow(g, rr, DLP.p)
        c = Web3.solidityKeccak(['bytes'], [
            BigNumber.from_py(g).val + BigNumber.from_py(y).val + BigNumber.from_py(grr).val])
        c = int.from_bytes(c, byteorder='big') % DLP.q
        rrr = (rr + (c * x) % DLP.q) % DLP.q
        assert(pow(g, rrr, DLP.p) == grr * pow(y, c, DLP.p) % DLP.p)
        self.grr, self.rrr = grr, rrr

    def to_sol(self):
        return BigNumber.from_py(self.grr).to_sol(), BigNumber.from_py(self.rrr).to_sol()
