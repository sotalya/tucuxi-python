# Tucuxi Python

This repository offers python wrappers to Tucuxi-core, for computing dosage predictions, percentiles, and adjustments.

It embeds tucuxi-core and will compile it during installation.

Using python can then be done using the embedded tucuxi-core, or by launching tucucli, the Tucuxi command line tool.


## Install the package

The python module can be build using pip. Currently two way are available.

- The first one will be to clone this repository and then execute the pip install command \
  ```
   $ git clone --recursive https://github.com/sotalya/tucuxi-python.git
   $ cd tucuxi-python
   $ pip install .
  ```
- The second one will be to install the package using the git link directly with pip install \
  ```
   $ pip install git+https://github.com/sotalya/tucuxi-python.git
  ```

Moreover, a setup.bat and setup.sh are available to directly install the package.

<sup>**NOTE: The ways of installing explained above will install the package as a global one. So, if you want to install it inside a virtual environment dont use them or from within the environment.**<sup>

## PyTest

A few test are also available to be run to validate if the package installation was successful. In order to run them, it is necessary to have the pytest \
package. However, this package should be automatically installed with the installation of sotalya. In the case it was not installed, it is possible to \
install it by using the command `pip intall pytest`. Once the pytest package is installed, it is possible to run the tests using the following method:
  ```
    $ cd tests
    $ py -m pytest -v
  ```

<sup>**NOTE: In order to run the tests, it is necessary to have the repository cloned, as the package itself will not include this tests.**<sup>
