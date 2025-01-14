.. image:: https://www.assimp.org/common/images/splash-color.png

.. _ai_main_install:

============
Installation
============

The **Asset-Importer-Library** can be integated in your applications in two ways:

* By installing pre-built libraries, if available for your platform.
* By integrating the library directly into your project using [CMake](https://cmake.org/) .

Detailed instructions for both methods can be found in the Build Instructions.

.. _ai_main_usage:

Usage
-----

Once the library is integrated into your IDE or project, you can start using it through one of two interfaces:

- A C++ interface
- A C interface with flat functions

The C++ API offers an RTTI-based approach and is strongly recommended if you're working in C++.
The C API, on the other hand, simplifies the creation of language bindings for other programming languages.
