import glob
import os
import sys
from pathlib import Path
from setuptools import setup, find_packages
from distutils import sysconfig

from Cython.Build import cythonize
import multiprocessing

# NB: this is required for computers with ARM architecture, as the
# default method is 'spawn' and this is incompatible with NTHREADS > 0
multiprocessing.set_start_method('fork')


ANNOTATE = int(os.getenv('ANNOTATE', 1))
GDB_DEBUG = int(os.getenv('GDB_DEBUG', 0))
FORCE = int(os.getenv('FORCE', 0))
PROFILE = int(os.getenv('PROFILE', 0))
TESTS = int(os.getenv('TESTS', 1))
COMPILE = int(os.getenv('COMPILE', 1))
IS_COMPILER_CLANG = (sysconfig.get_config_var('CC') == 'clang')


if 'build_ext' in sys.argv and '-j' in sys.argv:
    NTHREADS = int(sys.argv[sys.argv.index('-j') + 1])
else:
    NTHREADS = 0


ext_modules = []
if COMPILE:
    ext_modules = cythonize(
        ["cyboost/**/*.pyx"] + ["tests/**/*.pyx"],
        language_level=3,
        language='c++',
        annotate=ANNOTATE,
        gdb_debug=GDB_DEBUG,
        force=FORCE,
        compiler_directives={
            'linetrace': PROFILE,
            'binding': PROFILE,
            'profile': PROFILE,
            # 'warn.undeclared': True
        },
        nthreads=NTHREADS
    )


    def get_include():
        headers = (
            #glob.glob('./cyboost/**/*.h*', recursive=True)
        )

        dirs = list(set(os.path.dirname(h) for h in headers))

        return dirs


    for ext in ext_modules:
        # The Numpy C headers are currently required
        #ext.include_dirs.append(np.get_include())
        ext.include_dirs.extend(get_include())

        #ext.include_dirs.append(pa.get_include())
        # ext.libraries.extend(pa.get_libraries())
        # ext.library_dirs.extend(pa.get_library_dirs())
        ext.include_dirs.extend(["/usr/local/include/boost"])
        ext.library_dirs.extend(["/usr/local/lib"])


        # disable numpy warnings (we can remove this in cython 3 apparently.)
        #ext.define_macros.append(('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'))

        #ext.extra_compile_args.append('-std=c++11')
        if IS_COMPILER_CLANG:
            # disable ubiquitous clang warnings
            ext.extra_compile_args.append('-Wno-unreachable-code-fallthrough')
            ext.extra_compile_args.append('-Wno-unused-function')

        if PROFILE:
            ext.define_macros.append(('CYTHON_TRACE', '1'))
            ext.define_macros.append(('CYTHON_TRACE_NOGIL', '1'))

# REQUIREMENTS_FILE = f'{Path(__file__).parent}/requirements.txt'
#
# with open(REQUIREMENTS_FILE) as f:
#     requirements = f.readlines()


setup(
    name='cyboost',
    version='0.0.1',
    description='Boost for Cython',
    author='Anthony MacKinnon',
    ext_modules=ext_modules,
)
