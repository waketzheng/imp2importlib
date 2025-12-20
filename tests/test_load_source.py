import sys
from imp import load_source

import pytest


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Test this requires python>=3.12")
def test_load_source():
    assert callable(load_source)
    module = load_source("imp", "src/imp/__init__.py")
    assert module.load_source.__code__ == load_source.__code__
    assert module.load_source.__name__ == load_source.__name__
