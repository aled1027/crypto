import serpent
from ethereum import tester, utils, abi
from sha3 import sha3_256
import random

tester.enable_logging()

# 1. create a new state
s = tester.state()

# 2. link state with the contract
# generates a contract given the state.
c = s.abi_contract('rps.se')

"""
-1 ~ error
0 ~ tie
1 ~ player 1
2 ~ player 2
"""

##################################### UTILITY FUNCTIONS ########################################
tobytearr = lambda n, L: [] if L == 0 else tobytearr(n / 256, L - 1)+[n % 256]

def hex_to_byte_string(arg):
    return ''.join(map(chr, tobytearr(arg, 32)))

##################################### SETUP COMMITMENTS ########################################
choice = ["rock", "paper", "scissors"]



#0 = rock; 1 = paper; 2 = scissors
choice1 = 0x01
nonce1 = 0x01

ch1 = hex_to_byte_string(choice1)
no1 = hex_to_byte_string(nonce1)

print("Player zero chooses {} which is: {}").format(choice1, choice[choice1])

# this i'm iffy on
k0_pub_addr_hex = utils.encode_hex(tester.k0)

## Prepare and pad the address
k0_pub_addr = hex_to_byte_string(long(k0_pub_addr_hex.encode('hex'), 16))
# k0_pub_addr  = ''.join(map(chr, tobytearr(long(k0_pub_addr_hex.encode('hex'),16),32)))

## Now use it for the commitment
s1 = ''.join([k0_pub_addr, ch1, no1])
comm1 = utils.sha3(s1)

choice2 = 0x0
nonce2 = 0x01
ch2 = ''.join(map(chr, tobytearr(choice2, 32)))
no2 = ''.join(map(chr, tobytearr(nonce2, 32)))
print("Player one chooses {} which is: {}\n").format(choice2, choice[choice2])

k1_pub_addr_hex = utils.encode_hex(tester.k1)

## Prepare and pad the address
k1_pub_addr  = ''.join(map(chr, tobytearr(long(k1_pub_addr_hex.encode('hex'),16),32)))

## Now use it for the commitment
s2 = ''.join([k1_pub_addr, ch2, no2])
comm2 = utils.sha3(s2)

o = c.add_player(comm1, value=1000, sender=tester.k0)
print("Player 0 Added: {}").format(o)

o = c.add_player(comm2, value=1000, sender=tester.k1)
print("Player 1 Added: {}\n").format(o)

o = c.open(0x01,0x01, sender=tester.k0)
print("Open for player 0: {}").format(o)

o = c.open(0x00,0x01, sender=tester.k1)
print("Open for player 1: {}\n").format(o)

# needed to move the blockchain at least 10 blocks so check can run
s.mine(11)

o = c.check(sender=tester.k1)
print("Check says player {} wins\n").format(o)

c.balance_check(sender=tester.k0)
