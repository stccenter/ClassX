# classxlib\train\analysis\__init__.py
from Cython.Build import cythonize
from distutils.core import setup
import os

from Cython.Build import cythonize
from distutils.core import setup
import os
import hashlib

checked = False

def get_hash(path: str):
    BUF_SIZE = 65536 # lets read stuff in 64kb chunks! 32768 = 32kb
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1

def check_changes():
    file_location = os.path.dirname(os.path.abspath(__file__))
    current_hash = get_hash(f"{file_location}/attribute_calculations.pyx").hexdigest()
    if not os.path.exists(f"{file_location}/.cache"):        
        cached_hash = None
    else:
        with open(f"{file_location}/.cache", "r") as f:
            cached_hash = f.readline()
    
    if cached_hash != current_hash:
        print("pyx file is out of date remaking...")
        setup(
            name = "analysis",
            ext_modules = cythonize([(os.path.join("classxlib/train/analysis/")+"*.pyx")],compiler_directives={'language_level' : "3"}),
            script_args=['build_ext','--inplace', 'clean','--all'],
        )
        with open(f"{file_location}/.cache", "w") as f:
            f.write(current_hash)

# Only check for changes if we haven't yet
if not checked:
    check_changes()
    checked = True

try:
    from . import attribute_calculations as attr_calc
except ImportError:
    print("Import error rebuilding...")
    setup(
    name = "analysis",
    ext_modules = cythonize([(os.path.join("classxlib/train/analysis/")+"*.pyx")],compiler_directives={'language_level' : "3"}),
    script_args=['build_ext','--inplace', 'clean','--all'],
    )
    from . import attribute_calculations as attr_calc
