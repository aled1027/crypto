# import serpent
from ethereum import tester, utils, abi
from sha3 import sha3_256

s = tester.state()

c = s.abi_contract('hash_prob.se')

ret = c.sha3_check('1')
print ret
print hex(ret)
print ""

ret = c.sha256_check('1')
print ret
print hex(ret)
print ""

sh = sha3_256()
sh.update('1')
print (sh.hexdigest())
print ""

print utils.sha3('1').encode('hex')
