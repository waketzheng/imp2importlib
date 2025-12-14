import importlib.util
import importlib.machinery
import sys
from typing import Optional, Tuple, List, IO


def find_module(name: str, path: Optional[List[str]] = None) -> Tuple[Optional[IO], str, Tuple[str, str, int]]:
    """
    Find a module's location and information, similar to the deprecated imp.find_module().

    This function provides compatibility with the old imp.find_module() behavior
    using modern importlib functionality for Python 3.12+.

    Args:
        name: The name of the module to find (can be a simple name or dotted name)
        path: Optional list of paths to search. If None, searches sys.path

    Returns:
        A tuple (file, pathname, description) where:
        - file: File object opened for reading (or None for built-in/extension modules)
        - pathname: Full path to the module file or package directory
        - description: Tuple of (suffix, mode, type) where:
            * suffix: File extension (e.g., '.py', '.pyc', '')
            * mode: File open mode ('r' for source, 'rb' for compiled, '' for package/built-in)
            * type: Module type constant (PY_SOURCE, PY_COMPILED, C_EXTENSION, PKG_DIRECTORY, etc.)

    Raises:
        ModuleNotFoundError: If the module cannot be found

    Example:
        >>> file, pathname, description = find_module('os')
        >>> print(pathname)
        /usr/lib/python3.12/os.py
        >>> if file:
        ...     file.close()
    """
    PY_SOURCE = 1
    PY_COMPILED = 2
    C_EXTENSION = 3
    PKG_DIRECTORY = 5
    C_BUILTIN = 6
    PY_FROZEN = 7

    if name in sys.builtin_module_names:
        return (None, name, ('', '', C_BUILTIN))

    if importlib.machinery.FrozenImporter.find_spec(name) is not None:
        return (None, name, ('', '', PY_FROZEN))
    try:
        if path is not None:
            finder = importlib.machinery.PathFinder()
            spec = finder.find_spec(name, path)
        else:
            spec = importlib.util.find_spec(name)

        if spec is None:
            raise ModuleNotFoundError(f"No module named '{name}'")

    except (ModuleNotFoundError, ValueError, ImportError) as e:
        raise ModuleNotFoundError(f"No module named '{name}'") from e

    if spec.origin is None:
        if spec.submodule_search_locations:
            pathname = spec.submodule_search_locations[0]
            return (None, pathname, ('', '', PKG_DIRECTORY))
        else:
            return (None, name, ('', '', C_BUILTIN))

    pathname = spec.origin

    if pathname == 'built-in':
        return (None, name, ('', '', C_BUILTIN))

    if pathname == 'frozen':
        return (None, name, ('', '', PY_FROZEN))

    if spec.submodule_search_locations is not None:
        if pathname.endswith('__init__.py'):
            try:
                file_obj = open(pathname, 'r', encoding='utf-8')
                return (file_obj, pathname, ('.py', 'r', PKG_DIRECTORY))
            except (IOError, OSError):
                return (None, pathname, ('', '', PKG_DIRECTORY))
        else:
            import os
            package_dir = os.path.dirname(pathname) if os.path.isfile(pathname) else pathname
            return (None, package_dir, ('', '', PKG_DIRECTORY))

    if pathname.endswith('.py'):
        try:
            file_obj = open(pathname, 'r', encoding='utf-8')
            return (file_obj, pathname, ('.py', 'r', PY_SOURCE))
        except (IOError, OSError):
            return (None, pathname, ('.py', 'r', PY_SOURCE))

    elif pathname.endswith('.pyc'):
        try:
            file_obj = open(pathname, 'rb')
            return (file_obj, pathname, ('.pyc', 'rb', PY_COMPILED))
        except (IOError, OSError):
            return (None, pathname, ('.pyc', 'rb', PY_COMPILED))

    elif any(pathname.endswith(suffix) for suffix in importlib.machinery.EXTENSION_SUFFIXES):
        suffix = next(s for s in importlib.machinery.EXTENSION_SUFFIXES if pathname.endswith(s))
        return (None, pathname, (suffix, 'rb', C_EXTENSION))

    else:
        return (None, pathname, ('', '', PY_SOURCE))
