import gonko
from lammps import lammps
import os
import concurrent.futures as cf
from tqdm import tqdm
import itertools
import shutil
from gonko.utils.output import announce, yell


k = 2.5
iter_num = itertools.count()  # while loop iteration counter

datafile = gonko.file.DataFile("data.file")
print(f"natoms: {datafile.natoms}")
print(f"nbonds: {datafile.nbonds}")
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
