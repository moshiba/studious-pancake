import os
import shutil
import pytest
from gonko.file.ScriptOuput import ScriptOuput


@pytest.fixture(scope="function")
def file_factory():
    data_dir = "tests/data/ScriptOutput/"
    created_records = set()

    def _file_factory(name):
        file_path = data_dir + name + ".t"
        shutil.copy(file_path + ".ORIG", file_path + ".test")
        created_records.add(name)
        return ScriptOuput(file_path + ".test")

    yield _file_factory

    for record in created_records:
        print(f"teardown script output: {record}")
        file_path = data_dir + record + ".t"
        os.remove(file_path + ".test")


def test_fixture_initialization(file_factory):
    _ = file_factory("ShearModulusG")
    _ = file_factory("poissonRatioV")


class TestAvg:
    def test_avg_1(self, file_factory):
        """ special case: eval ALL terms (sorted) """
        # loose bound
        assert file_factory("avg1").avg(0, 10000) == 5.5

        # tight bound
        assert file_factory("avg1").avg(100, 1000) == 5.5

        # negative low bound with loose high bound
        assert file_factory("avg1").avg(-10, 10000) == 5.5

        # negative low bound with tight high bound
        assert file_factory("avg1").avg(-10, 1000) == 5.5

    def test_avg_2(self, file_factory):
        """ extreme case: eval ALL terms (RANDOM POSITION) """
        # loose bound
        assert file_factory("avg1").avg(0, 10000) == 5.5

        # tight bound
        assert file_factory("avg1").avg(100, 1000) == 5.5

        # negative low bound with loose high bound
        assert file_factory("avg1").avg(-10, 10000) == 5.5

        # negative low bound with tight high bound
        assert file_factory("avg1").avg(-10, 1000) == 5.5

    def test_avg_3(self, file_factory):
        """ normal case: eval some terms """
        # loose bound
        assert file_factory("avg3").avg(1001, 2000) == 5.5
