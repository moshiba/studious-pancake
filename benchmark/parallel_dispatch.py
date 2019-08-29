"""

    test the task dispatching functions
    Copyright (C) 2019 Hsuan-Ting Lu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import gonko
from lammps import lammps
import concurrent.futures as cf
import os
import shutil
from tqdm import tqdm
from gonko.utils.output import announce, yell

datafile = gonko.file.DataFile("data.file")

for iter_num in range(4):
    announce(f"round: {iter_num}, number of bonds = {datafile.nbonds}")
    with cf.ProcessPoolExecutor(max_workers=4) as executor:

        def LammpsJob(bond: int):
            """
            to be pickled,
            a function must be defined at the top level of the module
            """
            _LammpsJob = gonko.parallel.LammpsJobFactory(
                datafile.filename, "gonko/scripts/in.shear", "./",
                lammps)
            bond, avg = _LammpsJob(bond)
            return bond, avg

        minBond, minGi = min(list(
            tqdm(executor.map(
                LammpsJob, [int(b.split(" ")[0]) for b in datafile.Bonds[:8]],
                timeout=None,
                chunksize=1),
                 desc="Trying Bonds",
                 total=8,
                 position=0)),
                             key=(lambda x: x[1]))
