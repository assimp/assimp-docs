.. image:: https://www.assimp.org/common/images/splash-color.png

.. _ai_main_install:

============
Installation
============

The **Asset-Importer-Library** can be used in your applications in two ways:

* Using it by installing the pre-built libraries, when tey are available for your platform.
* Integrate the library into your project via **cmake**.

Both ways are described at `Build instructions <https://github.com/assimp/assimp/blob/master/Build.md>`_

.. _ai_main_usage:

Usage
-----

When you're done integrating the library into your IDE/project, you can now start using it. There are two separate
interfaces by which you can access the library: 

* A C++ interface 
* A C interface using flat functions. 

The C++-API supports an RTTI-based approach. If you want to work with C++ using these interfaces is strongly recommended.
The C-API shall help to generate any language binding more easily.
