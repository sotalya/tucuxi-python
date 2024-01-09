import io
import re
import sys

try:
    from skbuild import setup
except ImportError:
    print("Please update pip to pip 10 or greater, or a manually install the PEP 518 requirements in pyproject.toml",
          file=sys.stderr)
    raise

setup(
    packages=['sotalya', 'sotalya.pycli', 'sotalya.tucuxi', 'sotalya.data',
              'sotalya.importexport', 'sotalya.processing', 'sotalya.tucuxi.templates'],
    package_dir={'sotalya': "sotalya",
                 'sotalya.pycli': "sotalya/pycli",
                 'sotalya.tucuxi': "sotalya/tucuxi",
                 'sotalya.data': "sotalya/tucuxi/data",
                 'sotalya.importexport': "sotalya/tucuxi/importexport",
                 'sotalya.processing': "sotalya/tucuxi/processing",
                 'sotalya.tucuxi.templates': "sotalya/tucuxi/templates"},
    cmake_install_dir="sotalya/pycli",
    cmake_with_sdist=True,
)