.. _new_modules:

****************
Add a new module
****************

.. contents:: Index:
	:depth: 2
	
.. _intro:

Introduction
============

This document will explain how to add a new module to the sotalya package, by using the current structure and build methods.

Package builder
---------------

To build the package a mixed method was used, since there is a part that is a C++ extension based on pybind11 and a \
part that is pure python. In order to be able to build this mixed package a pyproject.toml, a setup.py and CMakeLists.txt \
where needed. 

pyproject.toml
^^^^^^^^^^^^^^

Inside the pyproject.toml file the static configurations can be found. Like the name of the package, version, and other project relevant informations. \ 
Moreover, it is also specified the dependencies and the required packages/softwares to make our package work.

setup.py
^^^^^^^^

Inside the setup.py there are the dinamic configuration. Here all the different folders where to find the python code are specified. Moreover, it also \
allow for the "usage name" definition. It is here that we specify which name to use to import a specific folder that will become a module inside our package. \
Lastly, here it is also specify where the C++ modules compiled with CMake are installed. Sadly, it is not possible to specify multiple folders for multiple \
extensions, which means that if a new C++ extension is added, a new method of building it need to be used, or it will be imported as sotalya.CMakeInstallDir.extension. 

CMakeLists.txt
^^^^^^^^^^^^^^

Lastly, the CMakeLists.txt is simply a normal CMake file that is used to compile the C++ code in a python extension.

Package tree
------------

Here below there is the rappresentation of the current package tree:

::

	├── sotalya
  │   ├── __init__.py
  │   ├── pycli/
  │   │	  ├── libs/
  │   │   ├── tucupywrap/	
  │   │   │   └── C++ sources	
  │   │	  ├── __init__.py
  │   │	  └── CMakeLists.txt
  │   ├── tucuxi/
  │   │   ├── data/
  │   │   │   └── python sources
  │   │   ├── importexport/
  │   │   │   └── python sources
  │   │   ├── processing/
  │   │   │   └── python sources
  │   │   ├── templates/
  │   │	  ├── __init__.py
  │   │	  └── utils.py
  │   └── tucuxi-core/
  ├── CMakeLists.txt
  ├── pyproject.toml
  └── setup.py
  
  
.. _pure_python_module:

Add a new pure python module
============================

In order to add a new module that is pure python, it is necessary to add a folder with the source code, and specify the usage name and the \
folder location inside the setup.py file. Moreover, in order to make it easier to find the module, a __init__.py file must be inside the new \
module folder.

::

  ├── sotalya
  │   ├── __init__.py
  │   ├── pycli/
  │   ├── tucuxi/
  │   ├── tucuxi-core/
  │   │
  │   └── newModule/
  │       ├── __init__.py
  │       ├── sub_module/
  │       │   └── python sources
  │       └── python sources
  │
  ├── CMakeLists.txt
  ├── pyproject.toml
  └── setup.py
				
__init__.py inside the new module folder
----------------------------------------

This file is only necessary for the pacakger to know how to build it. However, it can be left empty or, in order to simplify the \
import of the module and to make it more user-friendly, it can be like this:


.. code-block:: python

	from .source_1 import *
	from .source_2 import *
	## ....
	from .source_n import *
	
In this way, the package usage will simply be ``import sotalya.newModule`` instead of ``import sotalya.newModule.source_1.functionName``

__init__.py inside the sotalya folder
-------------------------------------

This __init__.py is used to simplify the imports of the submodules and to make it more user-friendly. In order to add the new module, \
simply add it to the submodules list:

.. code-block:: python

  submodules = [
                "pycli",
                "newModule",
                ]

.. _cpp_module:

Add a new C++ module
====================

In order to add a new module that is based on C++ and pybind11, it is a bit more complex that simply adding a pure-python one. Since the \
scikit-build relay on CMake to build the C++ sources, it is necessary  to create the __init__.py file, the CMakeLists.txt and to modify \
the setup.py file. However, if a new C++ extension is added to this packaging and building method, you will need to modify how the module \
import works in all scripts that use this package. Because now, it will be necessary to specify which extension you want to use like this: \
import sotalya.pycli.extension_old and import sotalya.pycli.extension_new. Otherwise, by using only import sotalya.pycli you will be \
importing both extensions.

::

	├── sotalya
	│	├── __init__.py
	│	├── tucuxi-core/
	│	├── pycli/
	│	│	├── libs/
	│	│	├── __init__.py
	│	│	├── CMakeLists.txt
	│	│	└── tucupywrap/	
	│	│
	│	└── newModuleCpp/
	│		├── __init__.py
	│		├── CMakeLists.txt
	│		└── sources.cpp
	│	
	├── CMakeLists.txt
	├── pyproject.toml
	└── README.md

CMakeLists.txt for the new module
---------------------------------

In order to build multiple modules and to make it easier to understand, it was decided that instead of putting everything inside the CMakeLists.txt \
at the root, to place the file inside the module itself and include it in the file at root level. As starting point, you can use the CMake file inside \
the existing module and change the sources with the new ones.

__init__.py inside the new module folder
----------------------------------------

This file is only necessary for the pacakger to know how to build it. However, it can be left empty or, in order to simplify the import of the module \
and to make it more user-friendly, it can be like this:

.. code-block:: python

	from .pythonCppCompiled import *
	
In this way, the package usage will simply be ``import sotalya.newModule`` instead of ``import sotalya.newModule.pythonCppCompiled.functionName``

__init__.py inside the sotalya folder
-------------------------------------

This __init__.py is used to simplify the imports of the submodules and to make it more user-friendly. In order to add the new module, simply add it to the \
submodules list:

.. code-block:: python

  submodules = [
                "tucuxiCore",
                "newModule",
                ]

