"""
Mocks the LAMMPS python binding
"""
import os
import shutil


class lammps:
    file_dir = "tests/data/ScriptOutput/"
    created_records = set()

    def __init__(self, name=None, cmdargs=None, ptr=None, comm=None):
        """
        create a LAMMPS object using the default liblammps.so library
        4 optional args are allowed: name, cmdargs, ptr, comm
        """
        if any(map((lambda x: x is not None), [name, ptr, comm])):
            raise NotImplementedError("optional args are not yet mocked")

    def close(self):
        """
        destroy a LAMMPS object
        """
        pass

    def file(self, file: str):
        """
        run an entire input script, file = "in.lj"
        """
        # @todo refactor the way mocking behavior
        # @body using context depending code is bad for maintainability
        if "in.shear" in file:
            self.outfile = "ShearModulusG.t"
        # elif "in.spread" in file:
        elif "in.uniaxial" in file:
            self.outfile = "poissonRatioV.t"
        else:
            raise NotImplementedError(f"unknown output for {file}")

        target_path = lammps.file_dir + self.outfile

        lammps.created_records.add(self.outfile)
        shutil.copy(target_path + ".ORIG", target_path + ".test")

    @classmethod
    def CleanupMocks(cls):
        for record in cls.created_records:
            print(f"teardown df: {record}")
            tg_path = cls.file_dir + record
            os.remove(tg_path + ".test")

    def command(self, cmd):
        """
        invoke a single LAMMPS command, cmd = "run 100"
        """
        raise NotImplementedError

    def commands_list(self, cmdlist):
        """
        invoke commands in cmdlist = "run 10", "run 20"
        """
        raise NotImplementedError

    def commands_string(self, multicmd):
        """
        invoke commands in multicmd = "run 10nrun 20"
        """
        raise NotImplementedError
