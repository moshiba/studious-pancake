import os
import shutil
import pytest
from gonko.fileio import DataFile


@pytest.fixture(scope="function")
def grouping_df():
    NAME = "grouping"
    df_path = "tests/data/" + NAME + ".datafile."
    shutil.copy(df_path + "ORIG", df_path + "test")
    yield DataFile(df_path + "test")
    print("teardown df")
    os.remove(df_path + "test")


@pytest.fixture(scope="function")
def writeback_df():
    NAME = "writeback"
    df_path = "tests/data/" + NAME + ".datafile."
    shutil.copy(df_path + "ORIG", df_path + "test")
    yield DataFile(df_path + "test")
    print("teardown df")
    os.remove(df_path + "test")


@pytest.fixture(scope="function")
def bondDel_df():
    NAME = "bondDel"
    df_path = "tests/data/" + NAME + ".datafile."
    shutil.copy(df_path + "ORIG", df_path + "test")
    yield DataFile(df_path + "test")
    print("teardown df")
    os.remove(df_path + "test")


@pytest.fixture(scope="function")
def bondAdd_df():
    NAME = "bondAdd"
    df_path = "tests/data/" + NAME + ".datafile."
    shutil.copy(df_path + "ORIG", df_path + "test")
    yield DataFile(df_path + "test")
    print("teardown df")
    os.remove(df_path + "test")


@pytest.fixture(scope="function")
def properties_df():
    NAME = "properties"
    df_path = "tests/data/" + NAME + ".datafile."
    shutil.copy(df_path + "ORIG", df_path + "test")
    yield DataFile(df_path + "test")
    print("teardown df")
    os.remove(df_path + "test")


def test_update_grouping(grouping_df):
    df = grouping_df
    assert len(df.groups) == 15
    for i in range(15):
        assert len(df.groups[i]) == 1
        assert df.groups[i][0] == 'g' + str(i+1) + '\n'


def test_writeback_clear(writeback_df):
    df = writeback_df
    for i in range(len(df.groups)):
        df.groups[i] = ['']
    df._DataFile__writeback()
    with open(df.filename, 'r') as f:
        assert all(map((lambda x: x == '\n'), f.readlines()))


def test_writeback_alter(writeback_df):
    df = writeback_df
    for i in range(len(df.groups)):  # 15 groups
        if i % 2 == 1:
            df.groups[i] = ['test even\n']
        elif i % 2 == 0:
            df.groups[i] = ['test odd\n']
    df._DataFile__writeback()
    with open(df.filename, 'r') as f:
        lines = f.readlines()
        for i in range(30):
            if i % 4 == 0:
                assert lines[i] == "test odd\n"
            elif i % 4 == 2:
                assert lines[i] == "test even\n"
            else:
                assert lines[i] == "\n"


class TestProperties:
    def test_is_latest(self, grouping_df):
        df = grouping_df
        assert df.is_latest is True
        assert df._DataFile__latest == df.is_latest

        df._DataFile__latest = False
        assert df.is_latest is False

        df._DataFile__latest = True
        assert df.is_latest is True

    def test_file_changed(self, grouping_df):
        df = grouping_df
        assert df._DataFile__latest is True

        df.file_changed()
        assert df._DataFile__latest is False

    def test_natoms(self, properties_df):
        df = properties_df
        assert df.natoms == 459

        df.groups[1][0] = "123 atoms\n"
        assert df.is_latest is True
        assert df.natoms == 123

        df.file_changed()
        assert df.natoms == 459

    def test_set_natoms(self, properties_df):
        df = properties_df
        assert df.natoms == 459
        df.set_natoms(10)
        assert df.groups[1][0] == "10 atoms\n"

    def test_nbonds(self, properties_df):
        df = properties_df
        assert df.nbonds == 1356

        df.groups[1][2] = "246 bonds\n"
        assert df.is_latest is True
        assert df.nbonds == 246

        df.file_changed()
        assert df.nbonds == 1356

    def test_set_nbonds(self, properties_df):
        df = properties_df
        assert df.nbonds == 1356
        df.set_nbonds(99)
        assert df.groups[1][2] == "99 bonds\n"

    def test_Masses(self, properties_df):
        df = properties_df
        assert df.groups[4] == ["g5\n"]
        assert df.Masses == ["g5\n"]

        df.Masses = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[4][i] == f"{2*(i+27)}\n"

    def test_PairCoeffs_soft(self, properties_df):
        df = properties_df
        assert df.groups[6] == ["g7\n"]
        assert df.PairCoeffs_soft == ["g7\n"]

        df.PairCoeffs_soft = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[6][i] == f"{2*(i+27)}\n"

    def test_BondCoeffs_harmonic(self, properties_df):
        df = properties_df
        assert df.groups[8] == ["g9\n"]
        assert df.BondCoeffs_harmonic == ["g9\n"]

        df.BondCoeffs_harmonic = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[8][i] == f"{2*(i+27)}\n"

    def test_Atoms_molecular(self, properties_df):
        df = properties_df
        df.Atoms_molecular
        assert df.groups[10] == ["g11\n"]
        assert df.Atoms_molecular == ["g11\n"]

        df.Atoms_molecular = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[10][i] == f"{2*(i+27)}\n"

    def test_Velocities(self, properties_df):
        df = properties_df
        assert df.groups[12] == ["g13\n"]
        assert df.Velocities == ["g13\n"]

        df.Velocities = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[12][i] == f"{2*(i+27)}\n"

    def test_Bonds(self, properties_df):
        df = properties_df
        assert df.groups[14] == ["g15\n"]
        assert df.Bonds == ["g15\n"]

        df.Bonds = ["54\n", "56\n", "58\n"]
        for i in range(3):
            assert df.groups[14][i] == f"{2*(i+27)}\n"


def test_deleteBond(bondDel_df):
    # self.Bonds = self.groups[14]
    df = bondDel_df
    pass


def test_addBond(bondAdd_df):
    # self.Bonds = self.groups[14]
    df = bondAdd_df
    pass


def test_deleteAtom(grouping_df):
    df = grouping_df
    with pytest.raises(NotImplementedError):
        df.deleteAtom(10)


def test_recoverAtom(grouping_df):
    df = grouping_df
    with pytest.raises(NotImplementedError):
        df.addAtom("not impl")