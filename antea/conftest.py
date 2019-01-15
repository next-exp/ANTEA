import os
import pytest


@pytest.fixture(scope = 'session')
def ANTEADIR():
    return os.environ['ANTEADIR']


@pytest.fixture(scope = 'session')
def ANTEADATADIR(ANTEADIR):
    return os.path.join(ANTEADIR, "testdata/")
