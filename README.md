# Tucuxi Python All

## Install the package

The python module can be build using pip. Currently two way are available.

- The first one will be to clone this repository and then execute the pip install command \
  ```
   $ git clone --recursive https://reds-gitlab.heig-vd.ch/reds-tucuxi/tucuxi-python-all.git
   $ cd tucuxi-python-all
   $ pip install .
  ```
- The second one will be to install the package using the git link directly with pip install \
  ```
   $ pip install git+https://reds-gitlab.heig-vd.ch/reds-tucuxi/tucuxi-python-all.git
  ```
  
Moreover, a setup.bat and setup.sh are available to directly install the package.

<sup>**NOTE: The ways of installing explained above will install the package as a global one. So, if you want to install it inside a vistual environment \
dont use them.**<sup>

## PyTest

A few test are also available to be run to validate if the package installation was successful. In order to run them, it is necessary to install the pytest package \
using th command `pip intall pytest`. Once the pytest package is installed, it is possible to run the tests using the following method:
  ```
    $ cd tests
    $ py -m pytest -v
  ```
  
<sup>**NOTE: In order to run the tests, it is necessary to have the repository cloned, as the package itself will not include this tests.**<sup>