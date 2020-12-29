from random import randrange
from lib.ct_same_dl_proof import CtSameDLProof
from constants.dlp import DLP


class Bid01Proof():
    def __init__(self, ctu, ctuu):
        w = randrange(1, DLP.q)
        self.ctv, self.ctvv = ctu.pow(w), ctuu.pow(w)
        self.pi = CtSameDLProof(ctu, ctuu, w)

    def ctv_ctvv_pi_sol(self):
        return self.ctv.to_sol(), self.ctvv.to_sol(), self.pi.to_sol()
