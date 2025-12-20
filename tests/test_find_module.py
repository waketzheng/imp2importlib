import site
import sys
from imp import load_source
from pathlib import Path

import pytest


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="Compatible test of find_module requires python<=3.11")
def test_find_module() -> None:
    builtin_imp = load_source("imp", str(Path(site.__file__).parent / "imp.py"))
    file, pathname, description = builtin_imp.find_module("os")
    if file:
        file.close()
    src_imp = load_source("imp", "src/imp/__init__.py")
    file2, pathname2, description2 = src_imp.find_module("os")
    if file2:
        file2.close()
        assert file.name == file2.name
    assert pathname == pathname2
    assert description == description2
