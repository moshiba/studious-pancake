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
import pathlib


def LammpsJobFactory(data_src: str, script: str, work_dir: str, library):
    def _LammpsJob(bond: int):
        """ a LAMMPS job wrapper for process-pool.map() """
        # Creates working directory
        workdir = f"{work_dir}job/{bond}/"

        if not os.path.isdir(workdir):
            os.makedirs(workdir)

        # Duplicates 'data.file' and deletes a bond
        data = shutil.copy(data_src, workdir + data_src)
        gonko.file.DataFile(data).deleteBond(bond)

        # Runs LAMMPS script
        output = f"{workdir}/{pathlib.PurePath(script).name}_out.t"
        gonko.file.ScriptFile(script, library).run(data, output, "log",
                                                   workdir)

        # Collects result and return
        avg = gonko.file.ScriptOuput(output).avg(int(2e+3), int(10e+3))
        return bond, avg

    return _LammpsJob
