#!/usr/bin/env python3
from lib.big_number import BigNumber
from web3 import Web3
from deploy import deploy
from auctioneer import Auctioneer
from bidder import Bidder
from seller import Seller
from constants.web3 import provider_url, http_timeout
from random import randrange
from constants.auction import price
import time
from lib.ct import Ct

web3 = Web3(Web3.HTTPProvider(provider_url,
                              request_kwargs={'timeout': http_timeout}))

if web3.isConnected() == False:
    print("web3 connection failed.")
    exit()
else:
    print("web3 connected!")

accounts = web3.eth.accounts
auctioneer_count = 2
bidder_count = 3

auction_contract = deploy(web3, [accounts[0], accounts[1]],
                          accounts[auctioneer_count + bidder_count])

auctioneers = [Auctioneer(i, accounts[i], web3, auction_contract)
               for i in range(auctioneer_count)]
bidders = [Bidder(i, accounts[i + auctioneer_count], web3, auction_contract)
           for i in range(bidder_count)]
seller = Seller(accounts[auctioneer_count + bidder_count])
print()

# x = 99999999999999999123999999
# y = 3333333333333
# a = to_big_number(x)
# b = to_big_number(y)
# c = auction_contract.functions.hashTest(a, b).call()
# print(c)
# print(from_big_number(c))

# c = Web3.solidityKeccak(['bytes', 'bytes'], [
#     Web3.toBytes(x), Web3.toBytes(y)])
# c = Web3.toInt(c)
# print(c)
# print(c.bit_length())

print('Phase 1 auctioneer initilization:', flush=True)
for auctioneer in auctioneers:
    auctioneer.phase_1_auctioneer_init()
success = auction_contract.functions.phase1Success().call()
if success == False:
    print('Phase 1 failed\n', flush=True)
    exit(1)
else:
    print('Phase 1 success\n', flush=True)

print('Phase 2 bidder join:', flush=True)
bid_debugs = []
for bidder in bidders:
    bid_debug = bidder.phase_2_bidder_join(randrange(len(price)))
    # bid_debug = bidder.phase_2_bidder_join(len(price) - 1)
    bid_debugs.append(bid_debug)

print('Wait for phase 2 ends:')
t = auctioneers[0].phase_2_time_left()
print('wait {:.2f} sec'.format(t), flush=True)
time.sleep(t + 3)

success = auction_contract.functions.phase2Success().call()
if success == False:
    print('Phase 2 failed\n')
    # exit()
else:
    print('Phase 2 success\n')

print('Phase 3.1 bidder verification sum 1:')
for auctioneer in auctioneers:
    auctioneer.phase_3_bidder_verification_sum_1()

print('Phase 3.2.1 bidder verification 01 omega:')
auctioneers[1].phase_3_bidder_verification_01_omega()

print('Phase 3.2.2 bidder verification 01 dec:')
for auctioneer in auctioneers:
    auctioneer.phase_3_bidder_verification_01_dec()

success = auction_contract.functions.phase3Success().call()
if success == False:
    print('Phase 3 failed\n')
    # exit()
else:
    print('Phase 3 success\n')

print('Phase 4 second highest bid decision omega:')
auctioneers[1].phase_4_second_highest_bid_decision_omega()

print('Phase 4 second highest bid decision dec:')
while True:
    success = auction_contract.functions.phase4Success().call()
    binarySearchL = auction_contract.functions.binarySearchL().call()
    binarySearchR = auction_contract.functions.binarySearchR().call()
    secondHighestBidPriceJ = auction_contract.functions.secondHighestBidPriceJ().call()
    print('({}, {}, {})'.format(binarySearchL,
                                secondHighestBidPriceJ, binarySearchR))
    if success or binarySearchL == len(price) - 1:
        break
    for auctioneer in auctioneers:
        auctioneer.phase_4_second_highest_bid_decision_dec()

success = auction_contract.functions.phase4Success().call()
if success == False:
    print('Phase 4 failed\n')
    exit(1)
else:
    print('Phase 4 success\n')

print('Phase 5 winner decision:')
for auctioneer in auctioneers:
    auctioneer.phase_5_winner_decision()

success = auction_contract.functions.phase5Success().call()
if success == False:
    print('Phase 5 failed\n')
    exit(1)
else:
    print('Phase 5 success\n')

print('price = {}'.format(price))
for bidder in bidders:
    print('B{} bid_price_j = {}'.format(bidder.index, bidder.bid_price_j))

winnerI = auction_contract.functions.winnerI().call()
print('winnerI = {}'.format(winnerI))

# for auctioneer in auctioneers:
#     print('A{} balance = {}'.format(auctioneer.index,
#                                     web3.eth.getBalance(auctioneer.addr)))
# for bidder in bidders:
#     print('B{} balance = {}'.format(bidder.index,
#                                     web3.eth.getBalance(bidder.addr)))
# balances = auction_contract.functions.getBalance().call()
# print('balances = {}'.format(balances))

print('Phase 6 payment:')
bidders[winnerI].phase_6_payment()

success = auction_contract.functions.phase6Success().call()
if success == False:
    print('Phase 6 failed\n')
    # exit(1)
else:
    print('Phase 6 success\n')

# for auctioneer in auctioneers:
#     print('A{} balance = {}'.format(auctioneer.index,
#                                     web3.eth.getBalance(auctioneer.addr)))
# for bidder in bidders:
#     print('B{} balance = {}'.format(bidder.index,
#                                     web3.eth.getBalance(bidder.addr)))

# balances = auction_contract.functions.getBalance().call()
# print('balances = {}'.format(balances))
