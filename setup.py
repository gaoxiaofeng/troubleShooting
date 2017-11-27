import sys,os
from os.path import abspath, join, dirname
from subprocess import list2cmdline
from distutils.command.install_scripts import install_scripts
from distutils.core import setup
requires = {}
if not sys.platform.startswith("java"):
    requires = {"install_requires": ['paramiko >= 1.8.0']}
try:
    from setuptools import setup    #use setuptools when available
except ImportError:
    pass



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
            if path.endswith('pyts.bat') or path.endswith('pytsmgr.bat'):
                with open(path, 'r') as input:
                    replaced = input.read().replace('python', interpreter)
                with open(path, 'w') as output:
                    output.write(replaced)

with open("README.rst","rb") as f:
    README = f.read()
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]


PACKAGES = ['troubleshooting', 'troubleshooting.framework', 'troubleshooting.framework.conf', 'troubleshooting.framework.exception',
            'troubleshooting.framework.httpserver', 'troubleshooting.framework.libraries', 'troubleshooting.framework.log',
            'troubleshooting.framework.management', 'troubleshooting.framework.modules', 'troubleshooting.framework.output',
            'troubleshooting.framework.remote', 'troubleshooting.framework.running', 'troubleshooting.framework.template',
            'troubleshooting.framework.variable', 'troubleshooting.framework.version', 'troubleshooting.framework.httpserver.www',
            'troubleshooting.framework.httpserver.www.cgi-bin', 'troubleshooting.framework.httpserver.www.css',
            'troubleshooting.framework.httpserver.www.fonts', 'troubleshooting.framework.httpserver.www.iframe',
            'troubleshooting.framework.httpserver.www.images', 'troubleshooting.framework.httpserver.www.js',
            'troubleshooting.framework.httpserver.www.others', 'troubleshooting.framework.httpserver.www.fonts.codropsicons',
            'troubleshooting.framework.httpserver.www.fonts.linecons', 'troubleshooting.framework.management.commands']





# print find_packages(where=SRC)
# sys.exit()
with open(join(CURDIR,"src","troubleshooting","framework","version","version.py"),"rb") as f:
    exec(f.read())
setup(
    name="troubleshooting-framework",
    version=VERSION,
    packages=PACKAGES,
    scripts=SCRIPTS,
    package_dir  = {'': 'src'},
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst','*.conf','*.js','*.css','*.html','*.eot','*.svg','*.ttf',"*.woff","*.DS_Store","*.png"],
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
    classifiers=CLASSIFIERS.splitlines(),
    # could also include long_description, download_url, classifiers, etc.
    cmdclass     = {'install_scripts': custom_install_scripts},
    long_description=README,
    **requires

)