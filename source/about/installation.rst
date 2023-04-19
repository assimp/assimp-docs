.. image:: https://www.assimp.org/common/images/splash-color.png

.. _ai_main_install:

************
Installation
************

The Asset-Importer-Library can be used in your applications by two ways:

* Using it by installing pre-built libraries 
* Integrate the library into your project via cmake.

Both ways are descriped at `Build instructions <https://github.com/assimp/assimp/blob/master/Build.md>`_

.. _ai_main_usage:

Usage
-----

When you're done integrating the library into your IDE/project, you can now start using it. There are two separate
interfaces by which you can access the library: 

* A C++ interface 
* A C interface using flat functions. 

The C++-API supports a RTTI-based approach. If you want to work with c++ using these interface is strongy recommended.
The C-API shall help to generate any language binding more easily.
