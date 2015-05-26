import serpent
from ethereum import tester, utils, abi
from sha3 import sha3_256
import random

tester.enable_logging()

# create a new state
s = tester.state()

# link state with the contract
# generates a contract given the state.
c = s.abi_contract('rps.se')

"""
-1 ~ error
0  ~ player 0
1  ~ player 1
2  ~ tie
"""

##################################### UTILITY FUNCTIONS ########################################
tobytearr = lambda n, L: [] if L == 0 else tobytearr(n / 256, L - 1)+[n % 256]

def hex_to_byte_string(arg):
    return ''.join(map(chr, tobytearr(arg, 32)))

##################################### SETUP COMMITMENTS ########################################
choice = ["rock", "paper", "scissors"]

# bs stands for byte string
choice0 = random.randint(0,2)
nonce0 = 0x01
choice0_bs = hex_to_byte_string(choice0)
nonce0_bs = hex_to_byte_string(nonce0)

choice1 = random.randint(0,2)
nonce1 = 0x01
choice1_bs = hex_to_byte_string(choice1)
nonce1_bs = hex_to_byte_string(nonce1)

print("Player zero chooses %d which is: %s" % (choice0, choice[choice0]))
print("Player one chooses %d which is: %s" % (choice1, choice[choice1]))

# the pub addresses should be
# 745948140856946866108753121277737810491401257713L
# 715574669332965331462488905126228088406116900462L

k0_pub_addr = hex_to_byte_string(long(utils.encode_hex(utils.privtoaddr(tester.k0)), 16))
s0 = ''.join([k0_pub_addr, choice0_bs, nonce0_bs])
comm0 = utils.sha3(s0)

k1_pub_addr = hex_to_byte_string(long(utils.encode_hex(utils.privtoaddr(tester.k1)), 16))
s1 = ''.join([k1_pub_addr, choice1_bs, nonce1_bs])
comm1 = utils.sha3(s1)

# add players to the game, add commits, and open commitments
o = c.add_player(comm0, value=1000, sender=tester.k0)
o = c.add_player(comm1, value=1000, sender=tester.k1)
o = c.open(choice0, nonce0, sender=tester.k0)
u = c.open(choice1, nonce1, sender=tester.k1)

# move the blockchain at least 10 blocks.
# the reason we require the movement is so that
# we give the players time  to post their commits
# I think.
s.mine(11)

o = c.check(sender=tester.k0)
print "Check says player %d wins" % o

c.balance_check(sender=tester.k0)
