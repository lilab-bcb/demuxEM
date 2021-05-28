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
    "importlib-metadata >=0.7; python_version < '3.8'",
    "pegasusio >=0.2.12",
]

setup(
    name="demuxEM",
    use_scm_version=True,
    zip_safe=False,
    description="demuxEM is the demultiplexing module of Pegasus",
    long_description=long_description,
    url="https://github.com/klarman-cell-observatory/demuxEM",
    author="Yiming Yang, Joshua Gould and Bo Li",
    author_email="cumulus-support@googlegroups.com",
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="demultiplexing cell/nucleus hashing single-cell data",
    packages=find_packages(),
    install_requires=requires,
    setup_requires = ["setuptools_scm"],
    python_requires="~=3.5",
    entry_points={"console_scripts": ["demuxEM=demuxEM.__main__:main"]},
)
