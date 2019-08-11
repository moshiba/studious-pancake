import pruningNET
from lammps import lammps

import os
import math

# Aquire some initial condition Z K
print("Aquiring some initial condition eg.Z and K")
with open("data.file", "r") as f:
    line = f.readlines()

    for i in range(len(line)):
        if i == 2:
            natoms = int(line[i].split(" ")[0])
        if i == 4:
            nbonds = int(line[i].split(" ")[0])
            break
f.close()
# for loading
nbonds = 1372

z = nbonds / natoms
k = 2.5
i_iter = 0
# Prunung  the network until some kind of condition is met.
print("#Prunung  the network until some kind of condition is met.")
while z >= k:

    print("===========Obtaining G0=============")
    print("===========G0 test begins=============")
    lmp = lammps()
    lmp.file("in.shear")
    lmp.close()
    print("===========G0 test is completed=============")

    i_iter += 1
    print("Number of iteration: ", i_iter)
    with open("ShearModulusG.t", "r") as f:  # ShearModulusG.t= G0
        store_MG = []
        line = f.readline()
        Sflag = False
        # BEFORE THIS LINE: read network info
        # AFTER THIS LINE: screen for some filter to continue loop
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
        for i in range(len(store_MG)):
            total_G += store_MG[i]
        G0 = total_G / len(store_MG)
    f.close()
    print("Initial G0 aqqired:", G0)

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
    #    f.close()
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
            f.close()

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

    f.close()
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
    f.close()
    z = b / a

    with open("./checkpoint/data_v{}_z{}.file".format(V, z), "w+") as f:
        for line in lines:
            f.write(line)
    f.close()

    print("Data saved at ./checkpoint")
    # copydata then save data in another folder

print("Pruing process finished.")
print("The final poisson ratio is =", V)
