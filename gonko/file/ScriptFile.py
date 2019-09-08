"""

    Handles everything related to a script file
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


class ScriptFile:
    def __init__(self, filename: str, library):
        self.filename = filename
        self.library = library

    def run(self,
            data_in: str = "data.file",
            data_out: str = "out.t",
            screen_out: str = "none",
            logfile: str = "log.lammps"):
        lmp = self.library(cmdargs=[
            "-echo", "both", "-screen", f"{screen_out}", "-var",
            "gonko_data_in", f"{data_in}", "-var", "gonko_data_out",
            f"{data_out}", "-log", f"{logfile}"
        ])
        lmp.file(self.filename)
        lmp.close()
