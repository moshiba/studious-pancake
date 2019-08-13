""" fileio
------------
helper functions for file I/O

"""
import itertools


class datafile:
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
        self.groups = list(zip(*stripped))[1]

        self.__latest = True  # lazy evaluation flag

    def __writeback(self):
        with open(self.filename, 'w') as f:
            for g in self.groups:
                for line in g:
                    f.write(line)
                f.write("\n")

    def deleteBond(self, bond_id: int) -> str:
        """
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
            raise self.BoundNotFoundError()

    def deleteAtom(self, atom_id: int) -> str:
        # @todo expect class to generalize someday
        """
        """
        raise NotImplementedError

    def recoverBond(self, bond: str):
        """
        """
        try:
            assert bond not in self.Bonds
        except AssertionError:
            raise self.BondAlreadyExistsError()

        self.Bonds.append(bond)
        self.Bonds.sort(key=(lambda x: int(x.split(' ')[0])))
        self.set_nbonds(self.nbonds + 1)

        self.__writeback()
        self.file_changed()

    def recoverAtom(self, atom: str):
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

    @property
    def PairCoeffs_soft(self):
        """
        """
        return self.groups[6]

    @property
    def BondCoeffs_harmonic(self):
        """
        """
        return self.groups[8]

    @property
    def Atoms_molecular(self):
        """
        """
        return self.groups[10]

    @property
    def Velocities(self):
        """
        """
        return self.groups[12]

    @property
    def Bonds(self):
        """
        """
        return self.groups[14]

    class NotFoundError(Exception):
        pass

    class BoundNotFoundError(NotFoundError):
        pass

    class AtomNotFoundError(NotFoundError):
        pass

    class AlreadyExistsError(Exception):
        pass

    class BondAlreadyExistsError(AlreadyExistsError):
        pass

    class AtomAlreadyExistsError(AlreadyExistsError):
        pass
