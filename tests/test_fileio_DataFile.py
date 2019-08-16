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
