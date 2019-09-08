import os
import shutil
import pytest
from gonko.file import DataFile


@pytest.fixture(scope="function")
def df_factory():
    data_dir = "tests/data/DataFile/"
    created_records = set()

    def _df_factory(name):
        df_path = data_dir + name + ".datafile"
        shutil.copy(df_path + ".ORIG", df_path + ".test")
        created_records.add(name)
        return DataFile(df_path + ".test")

    yield _df_factory

    for record in created_records:
        print(f"teardown df: {record}")
        df_path = data_dir + record + ".datafile"
        os.remove(df_path + ".test")


class TestBasicOperations:
    def test_update_grouping(self, df_factory):
        df = df_factory("grouping")
        assert len(df.groups) == 18
        for i in range(15):
            assert len(df.groups[i]) == 1
            assert df.groups[i][0] == 'g' + str(i + 1) + '\n'

    def test_writeback_clear(self, df_factory):
        df = df_factory("writeback")
        for i in range(len(df.groups)):
            df.groups[i] = ['']
        df._DataFile__writeback()
        with open(df.filename, 'r') as f:
            assert all(map((lambda x: x == '\n'), f.readlines()))

    def test_writeback_alter(self, df_factory):
        df = df_factory("writeback")
        for i in range(len(df.groups)):  # 15 groups
            if i % 2 == 0:
                df.groups[i] = ['test odd\n']
            elif i % 2 == 1:
                df.groups[i] = ['test even\n']
        df._DataFile__writeback()
        with open(df.filename, 'r') as f:
            lines = f.readlines()
            for i in range(29):
                if i % 4 == 0:
                    assert lines[i] == "test odd\n"
                elif i % 4 == 2:
                    assert lines[i] == "test even\n"
                else:
                    assert lines[i] == "\n"


class TestProperties:
    def test_natoms(self, df_factory):
        df = df_factory("properties")
        assert df.natoms == 459

        # without writeback
        df.groups[1][0] = "123 atoms\n"
        assert df.natoms == 459
        # alternation overwritten when property 'natoms' updated the object

        df.groups[1][0] = "123 atoms\n"
        df._DataFile__writeback()
        assert df.natoms == 123

    def test_set_natoms(self, df_factory):
        df = df_factory("properties")
        assert df.natoms == 459
        df.set_natoms(10)
        assert df.groups[1][0] == "10 atoms\n"

    def test_n_atom_types(self, df_factory):
        df = df_factory("properties")
        assert df.n_atom_types == 1

        # without writeback
        df.groups[1][1] = "246 atom types\n"
        assert df.n_atom_types == 1
        # alternation overwritten when property 'n_atom_types' updated the object

        df.groups[1][1] = "246 atom types\n"
        df._DataFile__writeback()
        assert df.n_atom_types == 246

    def test_set_n_atom_types(self, df_factory):
        df = df_factory("properties")
        assert df.n_atom_types == 1
        df.set_n_atom_types(10)
        assert df.groups[1][1] == "10 atom types\n"

    def test_nbonds(self, df_factory):
        df = df_factory("properties")
        assert df.nbonds == 1372

        # without writeback
        df.groups[1][2] = "246 bonds\n"
        assert df.nbonds == 1372
        # alternation overwritten when property 'nbonds' updated the object

        df.groups[1][2] = "246 bonds\n"
        df._DataFile__writeback()
        assert df.nbonds == 246

    def test_set_nbonds(self, df_factory):
        df = df_factory("properties")
        assert df.nbonds == 1372
        df.set_nbonds(99)
        assert df.groups[1][2] == "99 bonds\n"

    def test_n_bond_types(self, df_factory):
        df = df_factory("properties")
        assert df.n_bond_types == 1372

        # without writeback
        df.groups[1][3] = "246 bond types\n"
        assert df.n_bond_types == 1372
        # alternation overwritten when property 'n_bond_types' updated the object

        df.groups[1][3] = "246 bond types\n"
        df._DataFile__writeback()
        assert df.n_bond_types == 246

    def test_set_n_bond_types(self, df_factory):
        df = df_factory("properties")
        assert df.n_bond_types == 1372
        df.set_n_bond_types(99)
        assert df.groups[1][3] == "99 bond types\n"

    def test_nangles(self, df_factory):
        df = df_factory("properties")
        assert df.nangles == 2273

        # without writeback
        df.groups[1][4] = "246 angles\n"
        assert df.nangles == 2273
        # alternation overwritten when property 'nangles' updated the object

        df.groups[1][4] = "246 angles\n"
        df._DataFile__writeback()
        assert df.nangles == 246

    def test_set_nangles(self, df_factory):
        df = df_factory("properties")
        assert df.nangles == 2273
        df.set_nangles(99)
        assert df.groups[1][4] == "99 angles\n"

    def test_n_angle_types(self, df_factory):
        df = df_factory("properties")
        assert df.n_angle_types == 2273

        # without writeback
        df.groups[1][5] = "246 angle types\n"
        assert df.n_angle_types == 2273
        # alternation overwritten when property 'n_angle_types' updated the object

        df.groups[1][5] = "246 angle types\n"
        df._DataFile__writeback()
        assert df.n_angle_types == 246

    def test_set_n_angle_types(self, df_factory):
        df = df_factory("properties")
        assert df.n_angle_types == 2273
        df.set_n_angle_types(99)
        assert df.groups[1][5] == "99 angle types\n"

    def test_Masses(self, df_factory):
        df = df_factory("properties")
        assert df.groups[4] == ["g5\n"]
        assert df.Masses == ["g5\n"]

        df.Masses = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[4][i] == f"{2*(i+27)}\n"

    def test_PairCoeffs_soft(self, df_factory):
        df = df_factory("properties")
        assert df.groups[6] == ["g7\n"]
        assert df.PairCoeffs_soft == ["g7\n"]

        df.PairCoeffs_soft = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[6][i] == f"{2*(i+27)}\n"

    def test_BondCoeffs_harmonic(self, df_factory):
        df = df_factory("properties")
        assert df.groups[8] == ["g9\n"]
        assert df.BondCoeffs_harmonic == ["g9\n"]

        df.BondCoeffs_harmonic = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[8][i] == f"{2*(i+27)}\n"

    def test_AngleCoeffs_harmonic(self, df_factory):
        df = df_factory("properties")
        assert df.groups[10] == ["g11\n"]
        assert df.AngleCoeffs_harmonic == ["g11\n"]

        df.AngleCoeffs_harmonic = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[10][i] == f"{2*(i+27)}\n"

    def test_Atoms_molecular(self, df_factory):
        df = df_factory("properties")
        assert df.groups[12] == ["g13\n"]
        assert df.Atoms_molecular == ["g13\n"]

        df.Atoms_molecular = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[12][i] == f"{2*(i+27)}\n"

    def test_Velocities(self, df_factory):
        df = df_factory("properties")
        assert df.groups[14] == ["g15\n"]
        assert df.Velocities == ["g15\n"]

        df.Velocities = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[14][i] == f"{2*(i+27)}\n"

    def test_Bonds(self, df_factory):
        df = df_factory("properties")
        assert df.groups[16] == ["g17\n"]
        assert df.Bonds == ["g17\n"]

        df.Bonds = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[16][i] == f"{2*(i+27)}\n"

    def test_Angles(self, df_factory):
        df = df_factory("properties")
        assert df.groups[18] == ["g19\n"]
        assert df.Angles == ["g19\n"]

        df.Angles = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[18][i] == f"{2*(i+27)}\n"


class TestBondOperations:
    def test_deleteBond_succeed(self, df_factory):
        df = df_factory("bondDel")

        assert df.nbonds == 20

        db = df.deleteBond(1)
        assert db == "1 1 1 489\n"
        assert df.nbonds == 19

        assert "1 1 1 489\n" not in df.Bonds
        f = DataFile(df.filename)
        assert f.nbonds == 19
        assert "1 1 1 489\n" not in f.groups[14]
        del f
        with pytest.raises(DataFile.BondNotFoundError) as e:
            df.deleteBond(1)
        assert "bond index: 1" == str(e.value)
        assert df.nbonds == 19

        # EXPECT TO SUCCEED
        df.deleteBond(2)
        assert df.nbonds == 18
        assert "2 1 1 481\n" not in df.Bonds
        f = DataFile(df.filename)
        assert f.nbonds == 18
        assert "2 1 1 481\n" not in f.groups[14]
        del f
        with pytest.raises(DataFile.BondNotFoundError) as e:
            df.deleteBond(2)
        assert "bond index: 2" == str(e.value)
        assert df.nbonds == 18

    def test_deleteBond_fail(self, df_factory):
        df = df_factory("bondDel")
        assert df.nbonds == 20
        with pytest.raises(DataFile.BondNotFoundError) as e:
            df.deleteBond(2000)

        assert "bond index: 2000" == str(e.value)
        assert df.nbonds == 20

        f = DataFile(df.filename)
        assert f.nbonds == 20

    def test_addBond_succeed(self, df_factory):
        df = df_factory("bondAdd")
        assert df.nbonds == 17
        df.addBond("2 1 1 481\n")
        assert df.nbonds == 18

        f = DataFile(df.filename)
        assert "2 1 1 481\n" in f.groups[16]
        assert f.nbonds == 18

    def test_addBond_fail(self, df_factory):
        df = df_factory("bondAdd")
        assert df.nbonds == 17
        with pytest.raises(DataFile.BondAlreadyExistsError) as e:
            df.addBond("1 1 1 489\n")

        assert "bond: 1 1 1 489\n" == str(e.value)
        assert df.nbonds == 17

        f = DataFile(df.filename)
        assert f.nbonds == 17


class TestAtomOperations:
    def test_deleteAtom(self, df_factory):
        df = df_factory("grouping")
        with pytest.raises(NotImplementedError):
            df.deleteAtom(10)

    def test_recoverAtom(self, df_factory):
        df = df_factory("grouping")
        with pytest.raises(NotImplementedError):
            df.addAtom("not impl")
