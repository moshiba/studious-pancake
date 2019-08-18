"""
Mocks the LAMMPS python binding
"""
import os
import shutil


class lammps:
    data_dir = "tests/data/ScriptOutput/"
    created_records = set()

    def __init__(self, name=None, cmdargs=None, ptr=None, comm=None):
        """
        create a LAMMPS object using the default liblammps.so library
        4 optional args are allowed: name, cmdargs, ptr, comm
        """
        if any(map((lambda x: x is not None), [name, cmdargs, ptr, comm])):
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
        self.filename = file
        df_path = lammps.data_dir + self.filename + ".t."

        lammps.created_records.add(self.filename)
        shutil.copy(df_path + "ORIG", df_path + "test")

    def CleanupMocks(self):
        for record in lammps.created_records:
            print(f"teardown df: {record}")
            df_path = lammps.data_dir + record + ".t."
            os.remove(df_path + "test")

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
