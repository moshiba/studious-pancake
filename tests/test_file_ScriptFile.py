import os
import shutil
import pytest
from gonko.file import ScriptFile
from .mocks import lammps


@pytest.fixture(scope="function")
def script_factory():
    data_dir = "gonko/scripts/"
    created_records = set()

    def _script_factory(name):
        df_path = data_dir + "in." + name
        shutil.copy(df_path, df_path + "test")
        created_records.add(name)
        return ScriptFile(df_path + "test", lammps)

    yield _script_factory

    for record in created_records:
        print(f"teardown script: {record}")
        df_path = data_dir + "in." + record
        os.remove(df_path + "test")


def test_InitInstance_succeed(script_factory):
    script = script_factory("shear")
