from setuptools import setup, find_packages
import sys
from os.path import dirname,abspath,join
import os

CURDIR = dirname(abspath(__file__))
SRC = join(CURDIR,"src")
sys.path.append(SRC)
SCRIPTS = [join(SRC,"bin"),join(SRC,"bin","pyts")]
WINDOWS = os.sep == '\\'
if WINDOWS:
    SCRIPTS.append(join(SRC,"bin","pyts.bat"))
# print find_packages(where=SRC)
# sys.exit()
with open(join(CURDIR,"src","troubleshooting","framework","version","version.py"),"rb") as f:
    exec(f.read())
setup(
    name="troubleshooting-framework",
    version=VERSION,
    packages=find_packages(where=SRC),
    scripts=SCRIPTS,

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[''],
    package_dir  = {'': 'src'},
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst','*.conf'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    # metadata for upload to PyPI
    author="Gao Xiao Feng",
    author_email="zeus.gao@foxmail.com",
    description="This is an troubleShooting Framework Package",
    license="Apache License 2.0",
    keywords="troubleshooting gaoxiaofeng",
    url="https://github.com/gaoxiaofeng/troubleShooting",  # project home page, if any
    # could also include long_description, download_url, classifiers, etc.
)