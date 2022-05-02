import os
import tempfile

import pytest


@pytest.fixture(autouse=True)
def database():
    _, file_name = tempfile.mkstemp()
    os.environ["DATABASE_NAME"] = file_name
    yield
    os.unlink(file_name)
