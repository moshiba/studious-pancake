import utils

a = utils.file.datafile("data.file")
print(f"number of bonds: {a.nbonds}")
print(f"Bonds count: {len(a.Bonds)}")


aa = a.deleteBond(1)
print(aa)
bb = a.deleteBond(3)
print(bb)
cc = a.deleteBond(5)
print(cc)

'''
old_bond = a.deleteBond(1)
print(f"attempt to recover bond: {old_bond}")
a.recoverBond(old_bond)
print(old_bond)
print(f"number of bonds: {a.nbonds}")
'''
'''
old_bond = a.deleteBond(2)
print(f"attempt to recover bond: {old_bond}")
a.recoverBond(old_bond)
print(f"number of bonds: {a.nbonds}")
'''