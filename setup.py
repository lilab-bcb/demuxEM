import versioneer
from setuptools import setup, find_packages
from setuptools.extension import Extension
from codecs import open
import os


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

requires = [
    "docopt",
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "seaborn",
    "pegasusio"
]

setup(
    name="demuxEM",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
    description="demuxEM is the demultiplexing module of Pegasus",
    long_description=long_description,
    url="https://github.com/klarman-cell-observatory/demuxEM",
    author="Yiming Yang, Joshua Gould and Bo Li",
    author_email="cumulus-support@googlegroups.com",
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Jupyter",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="demultiplexing cell/nucleus hashing single-cell data",
    packages=find_packages(),
    install_requires=requires,
    python_requires="~=3.5",
    entry_points={"console_scripts": ["demuxEM=demuxEM.__main__:main"]},
)
