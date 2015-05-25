import ethereum
from ethereum import tester, utils, abi

tester.enable_logging()

serpent_code = '''
def multiply(a):
    return(a*2)
'''

# sets up initial state for test - a genesis block
s = tester.state()

# add contract to chain
c = s.abi_contract(serpent_code)

o = c.multiply(5, value=1000, sender=tester.k0)

:

