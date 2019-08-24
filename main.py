import gonko
from lammps import lammps
import os
import math
import itertools
import statistics
import shutil

# Aquire some initial condition Z K
print("Aquiring some initial condition eg. Z and K")
datafile = gonko.file.DataFile("data.file")
print(f"natoms: {datafile.natoms}")
print(f"nbonds: {datafile.nbonds}")


def announce(string: str, level: int = 12):
    print("=" * level, end='')
    print(string.strip('\n'), end='')
    print("=" * level)


def yell(string: str, width: int = 40):
    if len(string) > (width - 8):
        width = len(string) + 8
    print("=" * width)
    i = len(string) % 2
    wing = (width - len(string) - 8) // 2
    print("== " + " " * wing, string.strip('\n'), " " * (wing + i) + " ==")
    print("=" * width)


z = datafile.nbonds / datafile.natoms
k = 2.5

iter_num = itertools.count()  # while loop iteration counter

# Pruning the network until some kind of condition is met.
yell(f"{datafile.nbonds - (k * datafile.natoms) + 1} bonds to delete")


announce(f"Obtaining G0")
gonko.file.ScriptFile("gonko/scripts/in.shear", lammps).run("data.file", "ShearModulusG.t")
G0 = gonko.file.ScriptOuput("ShearModulusG.t").avg(2000, 10000)
announce(f"G0 test is completed")
announce(f"Initial G0 aqqired: {G0}")

while z >= k:
    deltaG = []

    announce(f"number of bonds = {datafile.nbonds}")
    yell(f"Deleting bonds...")
    for idx in [b.split(" ")[0] for b in datafile.Bonds]:
        announce(f"entering bond iteration: {idx}")
        temdeleted = datafile.deleteBond(idx)

        announce(f"Obtaining Gi")
        gonko.file.ScriptFile("gonko/scripts/in.shear",
                              lammps).run("data.file", "ShearModulusG.t")
        announce(f"Gi test is completed")

        tmp_G = gonko.file.ScriptOuput("ShearModulusG.t").avg(2000, 10000)
        deltaG.append((idx, tmp_G))
        # recover what was deleted in 'try'
        datafile.addBond(temdeleted)

    tmp_idx, min_dG = min(deltaG, key=(lambda x: x[1]))
    datafile.deleteBond(idx)  # = lowest deltaGi
    yell(f"Bond with lowest deltaG: {tmp_idx}(delta: {min_dG}) deleted")

    announce(f"Calculating V of the sample of this iteration.")
    V = gonko.file.ScriptFile("gonko/scripts/in.uniaxial", lammps).run("data.file", "poissonRatioV.t")
    announce(f"V test is completed")

    V = gonko.file.ScriptOuput("poissonRatioV.t").avg(2000, 10000)

    # Update G0
    gonko.file.ScriptFile("gonko/scripts/in.shear", lammps).run("data.file", "ShearModulusG.t")
    G0 = gonko.file.ScriptOuput("ShearModulusG.t").avg(2000, 10000)

    announce(f"Iteration is completed.")
    z = datafile.nbonds / datafile.natoms

    if not os.path.isdir('./checkpoint'):
        os.mkdir('./checkpoint')

    shutil.copy("data.file", f"./checkpoint/data_v{V}_z{z}.file")
    print("Data saved at ./checkpoint")

announce(f"Pruing process finished.")
# print("The final poisson ratio is =", V)
