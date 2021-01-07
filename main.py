#!/usr/bin/env python3
from constants.dlp import DLP
from lib.big_number import BigNumber
from web3 import Web3
from deploy import deploy
from bidder import Bidder
from seller import Seller
from constants.web3 import provider_url, http_timeout
from random import randrange
import time
from lib.tx_print import tx_print

web3 = Web3(Web3.HTTPProvider(provider_url,
                              request_kwargs={'timeout': http_timeout}))

if web3.isConnected() == False:
    print("web3 connection failed.")
    exit(1)
else:
    print("web3 connected!")

accounts = web3.eth.accounts
bidder_count = 3
m = 1

seller = Seller(accounts[0],
                m=m,
                zm_inv=BigNumber.from_py(pow(DLP.z, -m, DLP.p)).to_sol(),
                price=[p for p in range(1, bidder_count + 1)],
                time_limit=[20, 1000000, 1000000, 1000000, 1000000, 1000000],
                balance_limit=10)

auction_contract = deploy(web3, seller)

bidders = [Bidder(i, accounts[i + 1], web3, auction_contract)
           for i in range(bidder_count)]

# b2 = BigNumber.from_py(2).to_sol()
# b3 = BigNumber.from_py(3).to_sol()
# print("b2 = {}".format(b2))
# print("b3 = {}".format(b3))
# result = auction_contract.functions.mulTest(b2, b3).call()
# print("result = {}".format(BigNumber.from_sol(result).to_py()))
# print("result = {}".format(BigNumber.from_sol(result).val))
# print(BigNumber.from_sol(result).to_py())
# tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# tx_print(tx_receipt, "cmpTest")
# exit()
print()

print('Phase 1 bidder init:', flush=True)
for bidder in bidders:
    bidder.phase_1_bidder_init()

print('Wait for phase 1 ends:', flush=True)
t = bidders[0].phase_1_time_left()
print('wait {:.2f} sec'.format(t), flush=True)
time.sleep(t + 3)

success = auction_contract.functions.phase1Success().call()
if success == False:
    print('Phase 1 failed\n', flush=True)
    exit(1)
else:
    print('Phase 1 success\n', flush=True)

print('Phase 2 bidder submit bid:', flush=True)
price_length = auction_contract.functions.priceLength().call()
for bidder in bidders:
    bidder.phase_2_bidder_submit_bid(
        bidder.index % price_length)
success = auction_contract.functions.phase2Success().call()
if success == False:
    print('Phase 2 failed\n', flush=True)
    exit(1)
else:
    print('Phase 2 success\n', flush=True)

print('Phase 3 M+1st price decision prepare:', flush=True)
for bidder in bidders:
    bidder.phase_3_m_1st_price_decision_prepare()
success = auction_contract.functions.phase3Success().call()
if success == False:
    print('Phase 3 failed\n', flush=True)
    exit(1)
else:
    print('Phase 3 success\n', flush=True)

print('Phase 4 M+1st price decision:', flush=True)
while True:
    jM = auction_contract.functions.jM().call()
    print('jM before = {}'.format(jM), flush=True)
    for bidder in bidders:
        bidder.phase_4_m_1st_price_decision()
    success = auction_contract.functions.phase4Success().call()
    jM = auction_contract.functions.jM().call()
    print('jM after = {}'.format(jM), flush=True)
    price_length = auction_contract.functions.priceLength().call()
    if success or jM == price_length:
        break

success = auction_contract.functions.phase4Success().call()
if success == False:
    print('Phase 4 failed\n', flush=True)
    exit(1)
else:
    print('Phase 4 success\n', flush=True)

print('Phase 5 winner decision:', flush=True)
jM = auction_contract.functions.jM().call()
for bidder in bidders:
    if bidder.bid_price_j >= jM:
        bidder.phase_5_winner_decision()

success = auction_contract.functions.phase5Success().call()
if success == False:
    print('Phase 5 failed\n', flush=True)
    exit(1)
else:
    print('Phase 5 success\n', flush=True)

print('Phase 6 payment:', flush=True)
jM = auction_contract.functions.jM().call()
for bidder in bidders:
    if bidder.bid_price_j >= jM:
        bidder.phase_6_payment()

success = auction_contract.functions.phase6Success().call()
if success == False:
    print('Phase 6 failed\n', flush=True)
    exit(1)
else:
    print('Phase 6 success\n', flush=True)

for bidder in bidders:
    print('B{} used {:,} gas'.format(bidder.index, bidder.gasUsed), flush=True)

# for bidder in bidders:
#     print('B{} balance = {}'.format(bidder.index,
#                                     web3.eth.getBalance(bidder.addr)))

# balances = auction_contract.functions.getBalance().call()
# print('balances = {}'.format(balances))
