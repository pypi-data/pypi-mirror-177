import sys
from glob import glob
from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11.setup_helpers import ParallelCompile, naive_recompile
from setuptools import setup
from pathlib import Path


__version__ = '0.0.3'

ext_modules = [
    Pybind11Extension(
        "enhanced_icm20948.asm_orientation",
        sorted(glob("enhanced_icm20948/asm_orientation/*.cpp")),
        extra_compile_args = ["-O3"]
    )
]

ParallelCompile("NPY_NUM_BUILD_JOBS", needs_recompile=naive_recompile).install()
thisDirectory = Path(__file__).parent
longDescription = (thisDirectory / "README.md").read_text()

setup(
    name = "enhanced_icm20948",
    version = __version__,
    author = "Haoyuan Ma, Chenhao Zhang",
    author_email = "flyinghorse0510@zju.edu.cn",
    license = "MIT",
    url = "http://gogs.infcompute.com/mhy/enhanced_icm20948.git",
    description = "A test project using pybind11 & I2C",
    long_description = longDescription,
    long_description_content_type='text/markdown',
    ext_modules = ext_modules,
    cmdclass = {"build_ext": build_ext},
    zip_safe = False,
    python_requires = ">=3.7",
    packages = ["enhanced_icm20948"],
    install_requires = [
        'numpy',
    ]
)