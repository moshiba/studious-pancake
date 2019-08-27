import gonko
from lammps import lammps
import os
import math
import itertools
import statistics
import shutil


def announce(string: str, level: int = 12):
    print("=" * level, end=' ')
    print(string.strip('\n'), end=' ')
    print("=" * level)


def yell(string: str, width: int = 40):
    if len(string) > (width - 8):
        width = len(string) + 8
    print("=" * width)
    i = len(string) % 2
    wing = (width - len(string) - 8) // 2
    print("== " + " " * wing, string.strip('\n'), " " * (wing + i) + " ==")
    print("=" * width)


datafile = gonko.file.DataFile("data.file")
print(f"natoms: {datafile.natoms}")
print(f"nbonds: {datafile.nbonds}")

k = 2.5
iter_num = itertools.count()  # while loop iteration counter

# Pruning the network until some kind of condition is met.
yell(f"{datafile.nbonds - (k * datafile.natoms) + 1} bonds to delete")

announce(f"Obtaining G0")
gonko.file.ScriptFile("gonko/scripts/in.shear",
                      lammps).run("data.file", "ShearModulusG.t")
G0 = gonko.file.ScriptOuput("ShearModulusG.t").avg(2000, 10000)
announce(f"Initial G0 aqqired: {G0}")

while datafile.nbonds / datafile.natoms >= k:
    GiList = []

    announce(f"number of bonds = {datafile.nbonds}")
    yell(f"Deleting bonds...")
    for idx in [b.split(" ")[0] for b in datafile.Bonds]:
        announce(f"entering bond iteration: {idx}")
        GiList.append(
            tuple(
                gonko.parallel.LammpsJob("gonko/scripts/in.shear", lammps,
                                         "data.file", idx)))

    tmp_idx, min_Gi = min(GiList, key=(lambda x: x[1]))
    datafile.deleteBond(idx)  # = lowest Gi
    yell(f"Bond with lowest GiList: {tmp_idx}(Gi: {min_Gi}) deleted")

    announce(f"Calculating V of the sample of this iteration.")
    V = gonko.file.ScriptFile("gonko/scripts/in.uniaxial",
                              lammps).run("data.file", "poissonRatioV.t")
    announce(f"V test is completed")

    V = gonko.file.ScriptOuput("poissonRatioV.t").avg(2000, 10000)

    # Update G0
    G0 = min_Gi

    announce(f"Iteration is completed.")

    if not os.path.isdir('./checkpoint'):
        os.mkdir('./checkpoint')

    shutil.copy(f"job/{tmp_idx}/data.file",
                f"./checkpoint/data_v{V}_z{z}.file")
    print("Data saved at ./checkpoint")

announce(f"Pruing process finished.")
# print("The final poisson ratio is =", V)
