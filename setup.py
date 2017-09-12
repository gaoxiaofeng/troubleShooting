from setuptools import setup, find_packages
import sys
from os.path import dirname,abspath,join
import os
from os.path import abspath, join, dirname
from subprocess import list2cmdline
from distutils.core import setup
from distutils.command.install_scripts import install_scripts
CURDIR = dirname(abspath(__file__))
SRC = join(CURDIR,"src")
sys.path.append(SRC)
SCRIPTS = [join(SRC,"bin",pyfile) for pyfile in ("pyts","pytsmgr")]
WINDOWS = os.sep == '\\'
if WINDOWS:
    SCRIPTS.append(join(SRC,"bin","pyts.bat"))
    SCRIPTS.append(join(SRC,"bin","pytsmgr.bat"))
class custom_install_scripts(install_scripts):

    def run(self):
        install_scripts.run(self)
        if WINDOWS:
            self._replace_interpreter_in_bat_files()

    def _replace_interpreter_in_bat_files(self):
        print "replacing interpreter in pyts.bat and pytsmgr.bat"
        interpreter = list2cmdline([sys.executable])
        for path in self.get_outputs():
            if path.endswith('pyts.bat') or path.endswith('ptysmgr.bat'):
                with open(path, 'r') as input:
                    replaced = input.read().replace('python', interpreter)
                with open(path, 'w') as output:
                    output.write(replaced)

with open("README.rst","rb") as f:
    DES = f.read()



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
    install_requires=['paramiko'],
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
    cmdclass     = {'install_scripts': custom_install_scripts},
    long_description=DES,
)