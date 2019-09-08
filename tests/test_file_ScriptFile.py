import os
import shutil
import pytest
from gonko.file.ScriptFile import ScriptFile
from .mocks.lammps import lammps


@pytest.fixture(scope="function")
def script_factory():
    data_dir = "gonko/scripts/"
    created_records = set()

    def _script_factory(name):
        df_path = data_dir + "in." + name
        shutil.copy(df_path, df_path + ".test")
        created_records.add(name)
        return ScriptFile(df_path + ".test", lammps)

    yield _script_factory

    for record in created_records:
        print(f"teardown script: {record}")
        df_path = data_dir + "in." + record
        os.remove(df_path + ".test")


def test_InitInstance_succeed(script_factory):
    # expects nothing happens
    shear = script_factory("shear")
    spread = script_factory("spread")
    uniaxial = script_factory("uniaxial")
    assert all(map((lambda x: x.library == lammps), [shear, spread, uniaxial]))


def test_InitInstance_fail(script_factory):
    with pytest.raises(FileNotFoundError):
        _ = script_factory("dontexist")


def test_mock_run(script_factory):
    script = script_factory("shear")
    script.run()
    # expects nothing happens

    # @todo check that the mocked output has been generated
    # f = open(lammps.file_dir + file, 'r')
    lammps.CleanupMocks()
