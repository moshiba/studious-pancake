import utils
from lammps import lammps
import os
import math
import itertools
import statistics


# Aquire some initial condition Z K
print("Aquiring some initial condition eg. Z and K")
datafile = utils.fileio.datafile("data.file")
print(f"natoms: {datafile.natoms}")
print(f"nbonds: {datafile.nbonds}")


# for loading
nbonds = 1372

z = datafile.nbonds / datafile.natoms
k = 2.5
iter_num = itertools.count()


def get_GV_val(mode: str) -> int:
    if mode == "G":
        filename = "ShearModulusG.t"
    elif mode == "V":
        filename = "poissonRatioV.t"
    else:
        raise Exception

    with open(filename, "r") as f:  # ShearModulusG.t= G0
        f.readline()
        f.readline()
        lines = filter((lambda x: int(x.split(' ')[0]) > 20000), f.readlines())
        val_list = list(map((lambda x: float(x.split(' ')[1])), lines))
        val = statistics.mean(val_list)
        return val


# Pruning the network until some kind of condition is met.
print("#Pruning the network until some kind of condition is met.")
while z >= k:
    print("===========Obtaining G0=============")
    print("===========G0 test begins=============")
    lmp = lammps()
    lmp.file("in.shear")
    lmp.close()
    print("===========G0 test is completed=============")

    next(iter_num)
    print("Number of iteration: ", iter_num)
    G0 = get_GV_val('G')
    print("Initial G0 aqqired:", G0)

    # @todo LEGACY CODE
    # @body rewrite or cleanup
    # store initial bonds in each main iteration
    #    print("Storing initail bonds...")
    #    with open("data.file", "r") as f:
    #        store_bond = []
    #        line = f.readline()
    #        bflag = False
    #        while line:
    #            line = f.readline()
    #               bflag = True
    #            if bflag == True:
    #                store_bond.append(line)
    #    print("Storing initail bonds complete.")

    #    nbonds = len(store_bond)

    deltaG = []
    #    print("nmber of bonds =",b)
    print("Deleting bonds...")
    for idx in range(datafile.nbonds):
        print("*"*20)
        print("*"*20)
        print(f"entering bond iteration: {idx}")
        try:
            print(f"temdeleted (previous) : {temdeleted}")
        except:
            pass
        print("*"*20)
        print("*"*20)

        try:
            temdeleted = datafile.deleteBond(idx + 1)
            print("@"*30)
            print("@"*30)
            print("tem =", temdeleted)
            print("@"*30)
            print("@"*30)
        except utils.fileio.datafile.BoundNotFoundError as e:
            # Already deleted
            continue

        print(f"===========Obtaining Gi=============")
        print(f"===========Gi test begings=============")
        lmp = lammps()
        lmp.file("in.shear")
        lmp.close()
        print(f"===========Gi testd is completed=============")
        tmp_G = get_GV_val('G')
        deltaG.append((idx, tmp_G - G0))
        # recover what was deleted in 'try'
        print(f"about to try to recover bond: {temdeleted}")
        datafile.recoverBond(temdeleted)

    tmp_idx, min_G = min(deltaG, key=(lambda x: x[0]))
    datafile.deleteBond(idx + 1)  # = lowest deltaGi

    print("Bonds deleted.")

    print("Calculating V of the sample of this iteration.")
    lmp = lammps()
    lmp.file("in.uniaxial")
    lmp.close()
    print("===========V test is completed=============")
    V = get_GV_val('V')
    print("Iteration is completed.")

    if not os.path.isdir('./checkpoint'):
        os.mkdir('./checkpoint')

    z = datafile.nbonds / datafile.natoms

    # @todo check with designer to see if we need checkpoints
    # with open("./checkpoint/data_v{}_z{}.file".format(V, z), "w+") as f:
    #     for line in lines:
    #         f.write(line)

    # print("Data saved at ./checkpoint")
    # copydata then save data in another folder

print("Pruing process finished.")
print("The final poisson ratio is =", V)
