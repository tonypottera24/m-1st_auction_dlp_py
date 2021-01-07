from lib.same_dl_proof import SameDLProof
from lib.ct import Ct
from lib.dl_proof import DLProof
import random
from web3 import Web3
from constants.dlp import DLP
from lib.big_number import BigNumber


class CtMProof():
    def __init__(self, ctC, y, r, m):
        ctC = ctC * pow(DLP.z, -m, DLP.p) % DLP.p
        a = random.randrange(1, DLP.q)
        self.ctCA = pow(ctC, a, DLP.p)
        self.piA = SameDLProof(y, ctC, a)
        self.ya = pow(y, a, DLP.p)
        self.piR = DLProof(self.ya, r)
        assert(pow(y, r, DLP.p) == ctC)
        assert(pow(self.ya, r, DLP.p) == self.ctCA)

    def to_sol(self):
        return BigNumber.from_py(self.ya).to_sol(), BigNumber.from_py(self.ctCA).to_sol(), self.piA.to_sol(), self.piR.to_sol()
