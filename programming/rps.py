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
0 ~ player 0
1 ~ player 1
2 ~ tie
"""

##################################### UTILITY FUNCTIONS ########################################
tobytearr = lambda n, L: [] if L == 0 else tobytearr(n / 256, L - 1)+[n % 256]

def hex_to_byte_string(arg):
    return ''.join(map(chr, tobytearr(arg, 32)))

##################################### SETUP COMMITMENTS ########################################
choice = ["rock", "paper", "scissors"]

# bs stands for byte string
choice0 = random.randint(0,2)
choice0_bs = hex_to_byte_string(choice0)
nonce0_bs = hex_to_byte_string(0x01)

choice1 = random.randint(0,2)
choice1_bs = hex_to_byte_string(choice1)
nonce1_bs = hex_to_byte_string(0x01)

print("Player zero chooses %d which is: %s" % (choice0, choice[choice0]))
print("Player one chooses %d which is: %s" % (choice1, choice[choice1]))

## Prepare and pad the address
# TODO looks like tester.k0 is getting encoded into hex twice.
# TODO why is this being cast into a long?
k0_pub_addr_hex = utils.encode_hex(tester.k0)
k0_pub_addr = hex_to_byte_string(long(k0_pub_addr_hex.encode('hex'), 16))

k1_pub_addr_hex = utils.encode_hex(tester.k1)
k1_pub_addr = hex_to_byte_string(long(k1_pub_addr_hex.encode('hex'), 16))

s0 = ''.join([k0_pub_addr, choice0_bs, nonce0_bs])
s1 = ''.join([k1_pub_addr, choice1_bs, nonce1_bs])

# commitments
comm0 = utils.sha3(s0)
comm1 = utils.sha3(s1)

# TODO fix this comment
# add players to the game
o = c.add_player(comm0, value=1000, sender=tester.k0)
o = c.add_player(comm1, value=1000, sender=tester.k1)
o = c.open(0x01, 0x01, sender=tester.k0)
o = c.open(0x00, 0x01, sender=tester.k1)
# needed to move the blockchain at least 10 blocks so check can run
s.mine(11)
o = c.check(sender=tester.k1)
print("Check says player {} wins\n").format(o)
c.balance_check(sender=tester.k0)
