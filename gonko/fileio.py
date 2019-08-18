""" fileio
------------
helper functions for file I/O

"""
import statistics
import itertools


class DataFile:
    """
    represents a 'data.file'
    """
    def __init__(self, filename: str):
        self.filename = filename

        self.__latest = False
        # fetch latest state
        self.__update()

    def __update(self):
        groups = []
        uniquekeys = []
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for k, g in itertools.groupby(lines, (lambda x: x == "\n")):
                groups.append(list(g))  # Store group iterator as a list
                uniquekeys.append(k)
        stripped = filter((lambda x: x[0] is False), zip(uniquekeys, groups))
        self.groups = list(list(zip(*stripped))[1])

        self.__latest = True  # lazy evaluation flag

    def __writeback(self):
        with open(self.filename, 'w') as f:
            for g in self.groups:
                for line in g:
                    f.write(line)
                f.write("\n")
            f.flush()

    def deleteBond(self, bond_id: int) -> str:
        """
            parameter:
                bond_id: index of the bond,
                    * not the index of the array containing the 'Bonds' section
        """
        bond_id = str(bond_id)
        try:
            idx = list(map((lambda x: x.split(' ')[0]),
                           self.Bonds)).index(bond_id)
            popped = self.Bonds.pop(idx)
            self.set_nbonds(self.nbonds - 1)

            self.__writeback()
            self.file_changed()
            return popped
        except ValueError:
            # cannot find this bond
            raise self.BondNotFoundError(f"bond index: {bond_id}")

    def deleteAtom(self, atom_id: int) -> str:
        # @todo expect class to generalize someday
        """
        """
        raise NotImplementedError

    def addBond(self, bond: str):
        """
        """
        try:
            assert bond not in self.Bonds
        except AssertionError:
            raise self.BondAlreadyExistsError(f"bond index: {bond}")

        self.Bonds.append(bond)
        assert bond in self.Bonds
        assert bond in self.groups[14]
        print(len(self.Bonds))
        print(self.Bonds.index(bond))
        # self.Bonds.sort(key=(lambda x: int(x.split(' ')[0])))  DEBUG
        self.set_nbonds(self.nbonds + 1)

        self.__writeback()
        self.file_changed()

    def addAtom(self, atom: str):
        # @todo expect class to generalize someday
        """
        """
        raise NotImplementedError

    @property
    def is_latest(self):
        return self.__latest

    def file_changed(self):
        self.__latest = False

    @property
    def natoms(self):
        # @todo rename this for better clarity
        """ returns the number of atoms as integer
        """
        if not self.is_latest:
            self.__update()
        return int(self.groups[1][0].split(' ')[0])

    def set_natoms(self, num: int):
        self.groups[1][0] = str(num) + " atoms\n"
        self.file_changed()

    @property
    def nbonds(self):
        # @todo rename this for better clarity
        """ returns the number of bonds as integer
        """
        if not self.is_latest:
            self.__update()
        return int(self.groups[1][2].split(' ')[0])

    def set_nbonds(self, num: int):
        self.groups[1][2] = str(num) + " bonds\n"
        self.file_changed()

    @property
    def Masses(self):
        """
        """
        return self.groups[4]

    @Masses.setter
    def Masses(self, update: list):
        self.groups[4] = update

    @property
    def PairCoeffs_soft(self):
        """
        """
        return self.groups[6]

    @PairCoeffs_soft.setter
    def PairCoeffs_soft(self, update: list):
        self.groups[6] = update

    @property
    def BondCoeffs_harmonic(self):
        """
        """
        return self.groups[8]

    @BondCoeffs_harmonic.setter
    def BondCoeffs_harmonic(self, update: list):
        self.groups[8] = update

    @property
    def Atoms_molecular(self):
        """
        """
        return self.groups[10]

    @Atoms_molecular.setter
    def Atoms_molecular(self, update: list):
        self.groups[10] = update

    @property
    def Velocities(self):
        """
        """
        return self.groups[12]

    @Velocities.setter
    def Velocities(self, update: list):
        self.groups[12] = update

    @property
    def Bonds(self):
        """
        """
        return self.groups[14]

    @Bonds.setter
    def Bonds(self, update: list):
        self.groups[14] = update

    class NotFoundError(Exception):
        pass

    class BondNotFoundError(NotFoundError):
        pass

    class AtomNotFoundError(NotFoundError):
        pass

    class AlreadyExistsError(Exception):
        pass

    class BondAlreadyExistsError(AlreadyExistsError):
        pass

    class AtomAlreadyExistsError(AlreadyExistsError):
        pass


class ScriptFile:
    def __init__(self, filename):
        self.filename = filename


class ShearScript(ScriptFile):
    def __init__(self, filename):
        super().__init__(filename)


class UniaxialScript(ScriptFile):
    def __init__(self, filename):
        super().__init__(filename)


class ScriptOuput:
    def __init__(self, filename):
        self.filename = filename

    @property
    def avg(self, low_bound, high_bound) -> float:
        """ Average:

            parameters:
                low_bound:  valid number low bound
                high_bound: valid number high bound

        opens a file,
        retrieve designated lines according to the filter parameters,
        returns the average value

        """

        with open(self.filename, "r") as f:
            # read and ignore headers
            f.readline()
            f.readline()

            def range_selector(x):  # dynamically defined filter
                """ filter indexes of lines to be within designated range """
                num = int(x.split(' ')[0])
                return high_bound > num and num > low_bound

            lines = filter(range_selector, f.readlines())
            val_list = list(map((lambda x: float(x.split(' ')[1])), lines))
            val = statistics.mean(val_list)
            return val


class ShearOutput(ScriptOuput):
    def __init__(self, filename):
        assert filename == "ShearModulusG.t"
        super().__init__(filename)


class UniaxialOutput(ScriptOuput):
    def __init__(self, filename):
        assert filename == "poissonRatioV.t"
        super().__init__(filename)
