"""

    Handles everything related to a datafile
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
import itertools
import abc
import collections
import collections.abc


class _SectionType(collections.abc.MutableMapping):
    """ represents a section in the datafile """
    parser_result = collections.namedtuple("parser_result", ["key", "value"])
    __sections = set()

    @classmethod
    def _addSubClass(cls, subclass):
        if subclass not in cls.__sections:
            cls.__sections.add(subclass.__name__)

    @classmethod
    def sections(cls):
        """ returns a set of types of sections created """
        return cls.__sections

    @staticmethod
    @abc.abstractmethod
    def split(entry: str):
        pass

    @staticmethod
    @abc.abstractmethod
    def join(key, value) -> str:
        pass

    @abc.abstractmethod
    def __init__(self):
        super().__init__()
        self.__class__._addSubClass(self.__class__)
        self.entries = dict()

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __delitem__(self, key):
        del self.entries[key]

    def __iter__(self):
        return iter(self.entries.keys())

    def __len__(self) -> int:
        return len(self.entries)

    def __contains__(self, entry):
        key, value = self.split(entry)
        return (key, value) in self.entries.items()

    def keys(self):
        return self.entries.keys()

    def items(self):
        return self.entries.items()

    def values(self):
        return self.entries.values()

    def get(self, entry, default=None):
        return self.entries.get(self.split(entry).key, default)

    def pop(self, entry, default=None):
        return self.entries.pop(self.split(entry).key, default)

    def update(self, other) -> None:
        self.entries.update([(self.split(i).key, self.split(i).value)
                             for i in other])


class MassesSection(_SectionType):
    def __init__(Self):
        super().__init__()


class PairCoeffsSection(_SectionType):
    def __init__(Self):
        super().__init__()


class BondCoeffsSection(_SectionType):
    def __init__(Self):
        super().__init__()


class AngleCoeffsSection(_SectionType):
    def __init__(Self):
        super().__init__()


class AtomsSection(_SectionType):
    def __init__(Self):
        super().__init__()


class VelocitiesSection(_SectionType):
    def __init__(Self):
        super().__init__()


class BondsSection(_SectionType):
    @staticmethod
    def split(entry: str) -> _SectionType.parser_result:
        items = entry.rstrip('\n').split(' ')
        return _SectionType.parser_result(items[0], items[1:])

    @staticmethod
    def join(key, value) -> str:
        return ' '.join((key, *value))

    def __init__(self):
        super().__init__()


class AnglesSection(_SectionType):
    def __init__(Self):
        super().__init__()


class DataFile:
    """
    holds a filename and wrap utilities around it,
    DOES NOT represent a file handler.
    the actual file acted on depends solely on the filename it possess
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
        else:
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
        else:
            # HACK:
            # to avoid a premature _update() call that resets unwritten changes
            old_nbonds = self.nbonds
            self.Bonds.append(bond)
            # HACK:
            # use self.groups[14] instead of self.Bonds
            #   to avoid implicit __update() calls
            assert bond in self.groups[16]
            # print(f"Bonds Group size: {len(self.groups[16])}")
            # print(f"target bond index: {self.groups[16].index(bond)}")
            self.groups[16].sort(key=(lambda x: int(x.split(' ')[0])))
            self.set_nbonds(old_nbonds + 1)

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
