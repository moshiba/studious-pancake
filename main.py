import gonko
from lammps import lammps
import os
import math
import itertools
import statistics


# Aquire some initial condition Z K
print("Aquiring some initial condition eg. Z and K")
datafile = gonko.file.DataFile("data.file")
print(f"natoms: {datafile.natoms}")
print(f"nbonds: {datafile.nbonds}")


def anounce(string: str, level: int = 12):
    print("=" * level, end='')
    print(string.strip('\n'), end='')
    print("=" * level)


def yell(string: str, width: int = 40):
    if len(string) > (width - 8):
        width = len(string) + 8
    print("=" * width)
    i = len(string) % 2
    wing = (width - len(string) - 8) // 2
    print("== " + " " * wing, string.strip('\n'), " " * (wing+i) + " ==")
    print("=" * width)


z = datafile.nbonds / datafile.natoms
k = 2.5

iter_num = itertools.count()  # while loop iteration counter

# Pruning the network until some kind of condition is met.
print("#Pruning the network until some kind of condition is met.")
while z >= k:
    anounce("Obtaining G0")
    anounce("G0 test begins")
    gonko.file.ScriptFile("gonko/scripts/in.shear", lammps).run()
    anounce("G0 test is completed")

    print("Number of iteration: ", next(iter_num))

    G0 = gonko.file.ScriptOuput("ShearModulusG.t").avg(2000, 10000)
    print("Initial G0 aqqired:", G0)

    deltaG = []
    # print("number of bonds =", b)
    yell("  agh   ")
    yell("  agh   ")
    yell("Deleting bonds...")
    yell("  agh   ")
    yell("  agh   ")
    tmp_nbond = datafile.nbonds + 1
    for idx in range(1, tmp_nbond):
        yell(f"entering bond iteration: {idx}")

        try:
            if idx == 2:
                assert "2 1 1 481\n" in datafile.Bonds
            temdeleted = datafile.deleteBond(idx)
            yell(f"I've just deleted bond: {temdeleted} in round: {idx}")
            if idx == 2:
                assert "2 1 1 481\n" not in datafile.Bonds
            yell(f"tem = {temdeleted}")
        except gonko.file.DataFile.BondNotFoundError:
            # Already deleted
            continue

        anounce(f"Obtaining Gi")
        anounce(f"Gi test begings")
        gonko.file.ScriptFile("gonko/scripts/in.shear", lammps).run()
        anounce(f"Gi testd is completed")
        tmp_G = gonko.file.ScriptOuput("ShearModulusG.t").avg(2000, 10000)
        deltaG.append((idx, tmp_G - G0))
        # recover what was deleted in 'try'
        yell(f"about to try to recover bond: {temdeleted}")
        yell(f"loop counter (from 1): {idx}")
        datafile.addBond(temdeleted)

    tmp_idx, min_G = min(deltaG, key=(lambda x: x[0]))
    datafile.deleteBond(idx)  # = lowest deltaGi
    print("Bonds deleted.")

    print("Calculating V of the sample of this iteration.")
    V = gonko.file.ScriptFile("gonko/scripts/in.uniaxial", lammps).run()
    anounce("V test is completed")

    V = gonko.file.ScriptOuput("poissonRatioV.t").avg(2000, 10000)
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
# print("The final poisson ratio is =", V)
