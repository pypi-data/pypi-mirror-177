from pathlib import Path
from setuptools import setup, find_packages
import re

# from dcentrapi.common import get_dapi_version


def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


DESCRIPTION = 'Dcentralab Pypi packages'
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()
project_name = 'dcentrapi'
VERSION = '0.0.91'


# Setting up
setup(
    name="dcentrapi",
    version=VERSION,
    author="Dcentralab (Niv Shitrit)",
    author_email="<niv@dcentralab.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license='MIT',
    packages=find_packages(),
    install_requires=['requests', 'eth_abi>=3.0.1', 'web3>=5.31.1', 'cytoolz>=0.12.0', 'eth-utils>=2.1.0'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
