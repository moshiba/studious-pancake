import gonko
from lammps import lammps
import os
import concurrent.futures as cf
from tqdm import tqdm
import itertools
import shutil
from gonko.utils.output import announce, yell

k = 2.5
iter_num = itertools.count()  # while-loop iteration counter

datafile = gonko.file.DataFile("data.file")
print(f"natoms: {datafile.natoms}")
print(f"nbonds: {datafile.nbonds}")
yell(f"{datafile.nbonds - (k * datafile.natoms) + 1} bonds to delete")

announce(f"Obtaining G0")
gonko.file.ScriptFile("gonko/scripts/in.shear",
                      lammps).run(datafile.filename, "./ShearModulusG.t")
G0 = gonko.file.ScriptOuput("./ShearModulusG.t").avg(int(2e+3), int(10e+3))
announce(f"Initial G0 aqqired: {G0}")

z = datafile.nbonds / datafile.natoms
while z >= k:
    announce(f"round: {next(iter_num)}, number of bonds = {datafile.nbonds}")
    yell(f"Deleting bonds...")
    with cf.ProcessPoolExecutor(max_workers=None) as executor:

        def LammpsJob(bond: int):
            """
            to be pickled,
            a function must be defined at the top level of the module
            """
            _LammpsJob = gonko.parallel.LammpsJobFactory(
                datafile.filename, "gonko/scripts/in.shear", "./", lammps)
            bond, avg = _LammpsJob(bond)
            return bond, avg

        minBond, minGi = min(list(
            tqdm(executor.map(LammpsJob,
                              [int(b.split(" ")[0]) for b in datafile.Bonds],
                              timeout=None,
                              chunksize=1),
                 desc="Trying Bonds",
                 total=datafile.nbonds,
                 position=0)),
                             key=(lambda x: x[1]))

    yell(f"Bond with lowest GiList: {minBond}(Gi: {minGi}) deleted")
    G0 = minGi  # Update G0
    minValDir = f"./job/{minBond}/"  # Path to directory of interest

    announce("Calculating V of the sample of this iteration.")
    gonko.file.ScriptFile("gonko/scripts/in.uniaxial",
                          lammps).run("data.file", "poissonRatioV.t")
    V = gonko.file.ScriptOuput("poissonRatioV.t").avg(2000, 10000)
    # Update data file
    shutil.copy(minValDir + "data.file", "./data.file")

    announce(f"V test is completed")

    # Create checkpoint
    if not os.path.isdir('./checkpoint'):
        os.mkdir('./checkpoint')
    shutil.copy(minValDir + "data.file",
                f"./checkpoint/data_v{V.value}_z{z}.file")
    announce("Data saved at ./checkpoint")

    z = datafile.nbonds / datafile.natoms

announce(f"Pruing process finished.")
# print("The final poisson ratio is =", V)
