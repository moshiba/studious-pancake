import pruningNET
from lammps import lammps

import os
import math
import itertools
import statistics

# Aquire some initial condition Z K
print("Aquiring some initial condition eg. Z and K")
with open("data.file", "r") as f:
    f.readline()
    f.readline()
    natoms = int(f.readline().split()[0])
    f.readline()
    nbonds = int(f.readline().split()[0])
print(f"natoms: {natoms}")
print(f"nbonds: {nbonds}")


# for loading
nbonds = 1372

z = nbonds / natoms
k = 2.5
iter_num = itertools.count()
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
    with open("ShearModulusG.t", "r") as f:  # ShearModulusG.t= G0
        lines = f.readlines()[20000:100000]
        MG_list = list(map((lambda x: x.split(' ')[1]), lines))
        G0 = statistics.mean(MG_list)

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
    G = []
    temdeleted = " "
    #    print("nmber of bonds =",b)
    print("Deleting bonds...")
    for i in range(nbonds):

        if i != 0:
            pruningNET.resumebond(temdeleted)

        temdeleted = pruningNET.deletebond("Bonds", str(i + 1))
        print("tem =", temdeleted)

        if temdeleted == "PASS":
            G.append(math.inf)
            deltaG.append(math.inf)
            continue

        else:
            print("===========Obtaining Gi=============")
            print("===========Gi test begings=============")
            lmp = lammps()
            lmp.file("in.shear")
            lmp.close()
            print("===========Gi test is completed=============")

            with open("ShearModulusG.t", "r") as f:  # ShearModulusG.t= Gi
                store_MG = []
                line = f.readline()
                Sflag = False
                while line:
                    line = f.readline()

                    if line.split(" ")[0] == "20000":
                        Sflag = True
                    if line.split(" ")[0] == "100000":
                        Sflag = False
                    if Sflag:
                        store = line.split(" ")[1]
                        store_MG.append(float(store[:-1]))

            total_G = 0
            for m in range(len(store_MG)):
                total_G += store_MG[m]
            G.append(total_G / len(store_MG))
            deltaG.append(G[i] - G0)

    pruningNET.resumebond(temdeleted)

    pruningNET.deletebond("Bonds", str(deltaG.index(min(deltaG)) +
                                       1))  # = lowest deltaGi

    print("Bonds deleted.")

    print("Calculating V of the sample of this iteration.")
    lmp = lammps()
    lmp.file("in.uniaxial")
    lmp.close()
    print("===========V test is completed=============")
    with open("poissonRatioV.t", "r") as f:  # S poissonRatioV.t = V
        store_MV = []
        line = f.readline()
        Vflag = False
        while line:
            line = f.readline()

            if line.split(" ")[0] == "20000":
                Vflag = True
            if line.split(" ")[0] == "100000":
                Vflag = False
            if Vflag:
                store = line.split(" ")[1]
                store_MV.append(float(store[:-1]))


    total_V = 0
    for m in range(len(store_MV)):
        total_V += store_MV[m]
    V = total_V / len(store_MV)
    print("Iteration is completed.")

    if not os.path.isdir('./checkpoint'):
        os.mkdir('./checkpoint')

    with open("data.file", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 2:
                a = int(lines[i].split(" ")[0])
            if i == 4:
                b = int(lines[i].split(" ")[0])
                break

    z = b / a

    with open("./checkpoint/data_v{}_z{}.file".format(V, z), "w+") as f:
        for line in lines:
            f.write(line)


    print("Data saved at ./checkpoint")
    # copydata then save data in another folder

print("Pruing process finished.")
print("The final poisson ratio is =", V)
