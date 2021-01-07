import random
from web3 import Web3
from constants.dlp import DLP
from lib.big_number import BigNumber


class Ct01Proof():
    def __init__(self, v, a, b, r, y):
        n = pow(2, 256)
        if v == False:
            # 1. Simulate the v = 1 proof.
            c1 = random.randrange(0, n)
            rrr1 = random.randrange(1, DLP.q)

            bb = b * pow(DLP.z, -1, DLP.p)
            aa1 = pow(DLP.g, rrr1, DLP.p) * pow(a, -c1, DLP.p) % DLP.p
            bb1 = pow(y, rrr1, DLP.p) * pow(bb, -c1, DLP.p) % DLP.p

            # 2. Setup the v = 0 proof.
            rr0 = random.randrange(1, DLP.q)
            aa0 = pow(DLP.g, rr0, DLP.p)
            bb0 = pow(y, rr0, DLP.p)

            # 3. Create the challenge for v = 0 proof.
            c = Web3.solidityKeccak(['bytes'], [
                BigNumber.from_py(y).val + BigNumber.from_py(a).val + BigNumber.from_py(b).val + BigNumber.from_py(aa0).val + BigNumber.from_py(bb0).val + BigNumber.from_py(aa1).val + BigNumber.from_py(bb1).val])
            c = int.from_bytes(c, byteorder='big') % n
            c0 = (c - c1) % n

            # 4. Compute the v = 0 proof.
            rrr0 = (rr0 + c0 * r % DLP.q) % DLP.q

        else:  # v == 1
            # 1. Simulate the v = 0 proof.
            c0 = random.randrange(0, n)
            rrr0 = random.randrange(1, DLP.q)

            aa0 = pow(DLP.g, rrr0, DLP.p) * pow(a, -c0, DLP.p) % DLP.p
            bb0 = pow(y, rrr0, DLP.p) * pow(b, -c0, DLP.p) % DLP.p

            # 2. Setup the v = 1 proof.
            rr1 = random.randrange(1, DLP.q)
            aa1 = pow(DLP.g, rr1, DLP.p)
            bb1 = pow(y, rr1, DLP.p)

            # 3. Create the challenge for v = 1 proof.
            c = Web3.solidityKeccak(['bytes'], [
                BigNumber.from_py(y).val + BigNumber.from_py(a).val + BigNumber.from_py(b).val + BigNumber.from_py(aa0).val + BigNumber.from_py(bb0).val + BigNumber.from_py(aa1).val + BigNumber.from_py(bb1).val])
            c = int.from_bytes(c, byteorder='big') % n
            c1 = (c - c0) % n

            # 4. Compute the v = 0 proof.
            rrr1 = (rr1 + c1 * r % DLP.q) % DLP.q

        # 5. proof \pi
        self.aa0, self.aa1 = aa0, aa1
        self.bb0, self.bb1 = bb0, bb1
        self.c0, self.c1 = c0, c1
        self.rrr0, self.rrr1 = rrr0, rrr1

        assert(pow(DLP.g, rrr0, DLP.p) == aa0 * pow(a, c0, DLP.p) % DLP.p)
        assert(pow(DLP.g, rrr1, DLP.p) == aa1 * pow(a, c1, DLP.p) % DLP.p)
        assert(pow(y, rrr0, DLP.p) == bb0 * pow(b, c0, DLP.p) % DLP.p)
        assert(pow(y, rrr1, DLP.p) == bb1 *
               pow(b * pow(DLP.z, -1, DLP.p) % DLP.p, c1, DLP.p) % DLP.p)
        c = Web3.solidityKeccak(['bytes'], [
            BigNumber.from_py(y).val + BigNumber.from_py(a).val + BigNumber.from_py(b).val + BigNumber.from_py(aa0).val + BigNumber.from_py(bb0).val + BigNumber.from_py(aa1).val + BigNumber.from_py(bb1).val])
        c = int.from_bytes(c, byteorder='big') % n
        assert((c0 + c1) % n == c % n)

    def to_sol(self):
        return BigNumber.from_py(self.aa0).to_sol(), BigNumber.from_py(self.aa1).to_sol(), BigNumber.from_py(self.bb0).to_sol(), BigNumber.from_py(self.bb1).to_sol(), BigNumber.from_py(self.c0).to_sol(), BigNumber.from_py(self.c1).to_sol(), BigNumber.from_py(self.rrr0).to_sol(), BigNumber.from_py(self.rrr1).to_sol()
