""" Sub module for analysis of data. compiles our cython code and imports it. """

# classxlib\train\analysis\__init__.py

import os
import hashlib

# pylint: disable=deprecated-module
from Cython.Build import cythonize
from setuptools import Extension, setup

CHECKED = False
file_location = os.path.dirname(os.path.abspath(__file__))
extensions = [Extension("classxlib.train.analysis.attribute_calculations", [f"{file_location}/attribute_calculations.pyx"])]

def get_hash(path: str):
    """Get the hash of a file."""
    buffer_size = 65536  # lets read stuff in 64kb chunks! 32768 = 32kb
    sha1 = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha1.update(data)
    return sha1


def check_changes():
    """Check if the file hashes have changed and if so recompile the pyx file."""
    file_location = os.path.dirname(os.path.abspath(__file__))
    current_hash = get_hash(f"{file_location}/attribute_calculations.pyx").hexdigest()
    if not os.path.exists(f"{file_location}/.cache"):
        cached_hash = None
    else:
        with open(f"{file_location}/.cache", "r", encoding="utf-8") as f:
            cached_hash = f.readline()

    if cached_hash != current_hash:
        print("pyx file is out of date remaking...")
        setup(
            name="analysis",
            ext_modules=cythonize(
                extensions,
                compiler_directives={"language_level": "3"},
            ),
            script_args=["build_ext", "--inplace", "clean", "--all"],
        )
        with open(f"{file_location}/.cache", "w", encoding="utf-8") as f:
            f.write(current_hash)


# Only check for changes if we haven't yet
if not CHECKED:
    check_changes()
    CHECKED = True

try:
    from . import attribute_calculations as attr_calc
except ImportError:
    print("Import error rebuilding...")
    setup(
            name="analysis",
            ext_modules=cythonize(
                extensions,
                compiler_directives={"language_level": "3"},
            ),
            script_args=["build_ext", "--inplace", "clean", "--all"],
        )
    from . import attribute_calculations as attr_calc
