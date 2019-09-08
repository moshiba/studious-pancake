""" file
------------
helper functions for files

"""
import statistics
import itertools


class DataFile:
    """
    represents a 'data.file'
    """
    def __init__(self, filename: str):
        self.filename = filename
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

    def __writeback(self):
        with open(self.filename, 'w') as f:
            first = True
            for g in self.groups:
                if first:
                    first = False
                else:
                    f.write("\n")
                for line in g:
                    f.write(line)
            f.flush()

    def deleteBond(self, bond_id: int) -> str:
        """
            parameter:
                bond_id: index of the bond,
                    * not the index of the array containing the 'Bonds' section
        """
        try:  # find target bond
            idx = list(map((lambda x: x.split(' ')[0]),
                           self.Bonds)).index(str(bond_id))
        except ValueError:
            raise self.BondNotFoundError(f"bond index: {bond_id}")
            # Exits function

        # to avoid a premature _update() call that resets unwritten changes
        old_nbonds = self.nbonds
        popped = self.Bonds.pop(idx)
        self.set_nbonds(old_nbonds - 1)

        self.__writeback()
        return popped

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
            raise self.BondAlreadyExistsError(f"bond: {bond}")
            # Exits function

        # HACK:
        # to avoid a premature _update() call that resets unwritten changes
        old_nbonds = self.nbonds
        self.Bonds.append(bond)
        # HACK:
        # use self.groups[16] instead of self.Bonds
        #   to avoid implicit __update() calls
        assert bond in self.groups[16]
        # print(f"Bonds Group size: {len(self.groups[16])}")
        # print(f"target bond index: {self.groups[16].index(bond)}")
        self.groups[16].sort(key=(lambda x: int(x.split(' ')[0])))
        self.set_nbonds(old_nbonds + 1)

        self.__writeback()

    def addAtom(self, atom: str):
        # @todo expect class to generalize someday
        """
        """
        raise NotImplementedError

    @property
    def natoms(self):
        # @todo rename this for better clarity
        """ returns the number of atoms as integer
        """
        self.__update()
        return int(self.groups[1][0].split(' ')[0])

    def set_natoms(self, num: int):
        self.groups[1][0] = str(num) + " atoms\n"
        self.__writeback()

    @property
    def n_atom_types(self):
        # @todo rename this for better clarity
        """ returns the number of atom types as integer
        """
        self.__update()
        return int(self.groups[1][1].split(' ')[0])

    def set_n_atom_types(self, num: int):
        self.groups[1][1] = str(num) + " atom types\n"
        self.__writeback()

    @property
    def nbonds(self):
        # @todo rename this for better clarity
        """ returns the number of bonds as integer
        """
        self.__update()
        return int(self.groups[1][2].split(' ')[0])

    def set_nbonds(self, num: int):
        self.groups[1][2] = str(num) + " bonds\n"
        self.__writeback()

    @property
    def n_bond_types(self):
        # @todo rename this for better clarity
        """ returns the number of bond types as integer
        """
        self.__update()
        return int(self.groups[1][3].split(' ')[0])

    def set_n_bond_types(self, num: int):
        self.groups[1][3] = str(num) + " bond types\n"
        self.__writeback()

    @property
    def nangles(self):
        # @todo rename this for better clarity
        """ returns the number of angles as integer
        """
        self.__update()
        return int(self.groups[1][4].split(' ')[0])

    def set_nangles(self, num: int):
        self.groups[1][4] = str(num) + " angles\n"
        self.__writeback()

    @property
    def n_angle_types(self):
        # @todo rename this for better clarity
        """ returns the number of angle types as integer
        """
        self.__update()
        return int(self.groups[1][5].split(' ')[0])

    def set_n_angle_types(self, num: int):
        self.groups[1][5] = str(num) + " angle types\n"
        self.__writeback()

    @property
    def Masses(self):
        """
        """
        self.__update()
        return self.groups[4]

    @Masses.setter
    def Masses(self, update: list):
        self.groups[4] = update
        self.__writeback()

    @property
    def PairCoeffs_soft(self):
        """
        """
        self.__update()
        return self.groups[6]

    @PairCoeffs_soft.setter
    def PairCoeffs_soft(self, update: list):
        self.groups[6] = update
        self.__writeback()

    @property
    def BondCoeffs_harmonic(self):
        """
        """
        self.__update()
        return self.groups[8]

    @BondCoeffs_harmonic.setter
    def BondCoeffs_harmonic(self, update: list):
        self.groups[8] = update
        self.__writeback()

    @property
    def AngleCoeffs_harmonic(self):
        """
        """
        self.__update()
        return self.groups[10]

    @AngleCoeffs_harmonic.setter
    def AngleCoeffs_harmonic(self, update: list):
        self.groups[10] = update
        self.__writeback()

    @property
    def Atoms_molecular(self):
        """
        """
        self.__update()
        return self.groups[12]

    @Atoms_molecular.setter
    def Atoms_molecular(self, update: list):
        self.groups[12] = update
        self.__writeback()

    @property
    def Velocities(self):
        """
        """
        self.__update()
        return self.groups[14]

    @Velocities.setter
    def Velocities(self, update: list):
        self.groups[14] = update
        self.__writeback()

    @property
    def Bonds(self):
        """
        """
        self.__update()
        return self.groups[16]

    @Bonds.setter
    def Bonds(self, update: list):
        self.groups[16] = update
        self.__writeback()

    @property
    def Angles(self):
        """
        """
        self.__update()
        return self.groups[18]

    @Angles.setter
    def Angles(self, update: list):
        self.groups[18] = update
        self.__writeback()

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
    def __init__(self, filename, library):
        self.filename = filename
        self.library = library

    def run(self):
        lmp = self.library()
        lmp.file(self.filename)
        lmp.close()


class ScriptOuput:
    def __init__(self, filename: str):
        self.filename = filename

    def avg(self, low_bound: int, high_bound: int) -> float:
        # @todo add more warnings about inclusive/exclusive bound rules
        """ Average:

        [ INCLUSIVE BOUND ]

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
                return high_bound >= num and num >= low_bound

            lines = filter(range_selector, f.readlines())
            val_list = list(map((lambda x: float(x.split(' ')[1])), lines))
            val = statistics.mean(val_list)
            return val
