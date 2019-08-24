"""

    parallel utilities
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
import os
import shutil
import gonko


def LammpsJob(script: str, library, data_src: str, bond: int):
    """ a LAMMPS job wrapper for process-pool.map() """
    workdir = f"job/{bond}/"
    if os.path.isdir(workdir):
        os.makedirs(workdir)

    data = shutil.copy(data_src, workdir + "data.file")
    output = f"workdir/{script}_out.t"
    gonko.file.ScriptFile(script, library).run(data, output, "none")

    return bond, gonko.file.ScriptOuput(output).avg
