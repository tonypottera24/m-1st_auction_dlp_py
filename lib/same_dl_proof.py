from random import randrange
from web3 import Web3
from lib.big_number import BigNumber
from constants.dlp import DLP


class SameDLProof():
    def __init__(self, g1, g2, x):
        y1, y2 = pow(g1, x, DLP.p), pow(g2, x, DLP.p)
        rr = randrange(1, DLP.q)
        grr1, grr2 = pow(g1, rr, DLP.p), pow(g2, rr, DLP.p)
        c = Web3.solidityKeccak(['bytes'], [
                                BigNumber.from_py(g1).val + BigNumber.from_py(g2).val + BigNumber.from_py(y1).val + BigNumber.from_py(y2).val + BigNumber.from_py(grr1).val + BigNumber.from_py(grr2).val])
        c = int.from_bytes(c, byteorder='big') % DLP.q
        rrr = (rr + c * x % DLP.q) % DLP.q

        assert(pow(g1, rrr, DLP.p) == grr1 * pow(y1, c, DLP.p) % DLP.p)
        assert(pow(g2, rrr, DLP.p) == grr2 * pow(y2, c, DLP.p) % DLP.p)
        self.grr1, self.grr2, self.rrr = grr1, grr2, rrr

    def to_sol(self):
        return BigNumber.from_py(self.grr1).to_sol(), BigNumber.from_py(self.grr2).to_sol(), BigNumber.from_py(self.rrr).to_sol()
