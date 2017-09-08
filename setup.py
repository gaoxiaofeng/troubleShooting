from setuptools import setup, find_packages

PACKAGES = ["framework.conf","runner.py"]

setup(
    name="TroubleShooting Framework",
    version="1.0",
    packages=find_packages(),
    scripts=[''],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[''],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author="Gao Xiao Feng",
    author_email="zeus.gao@foxmail.com",
    description="This is an troubleShooting Framework Package",
    license="Apache License 2.0",
    keywords="troubleshooting gaoxiaofeng",
    packages=PACKAGES,
    url="",   # project home page, if any


    # could also include long_description, download_url, classifiers, etc.
)