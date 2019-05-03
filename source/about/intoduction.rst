.. _ai_introduction:

Introduction
============

assimp is a library to load and process geometric scenes from various data formats. It is tailored at typical game
scenarios by supporting a node hierarchy, static or skinned meshes, materials, bone animations and potential texture data.
The library is *not* designed for speed, it is primarily useful for importing assets from various sources once and
storing it in a engine-specific format for easy and fast every-day-loading. assimp is also able to apply various post
processing steps to the imported data such as conversion to indexed meshes, calculation of normals or tangents/bitangents
or conversion from right-handed to left-handed coordinate systems.

assimp currently supports the following file formats (note that some loaders lack some features of their formats because
some file formats contain data not supported by assimp, some stuff would require so much conversion work
that it has not been implemented yet and some (most ...) formats lack proper specifications):

* **Collada** ( .dae, .xml )
* **Blender** ( .blend )
* **Biovision BVH** ( .bvh ) 
* **3D Studio Max 3DS** ( .3ds )
* **3D Studio Max ASE** ( .ase )
* **Wavefront Object** ( .obj ) 
* **Stanford Polygon Library** ( .ply )
* **AutoCAD DXF** ( .dxf )
* **IFC-STEP** ( .ifc )
* **Neutral File Format** ( .nff )
* **Sense8 WorldToolkit** ( .nff )
* **Valve Model** ( .smd, .vta )
* **Quake I** ( .mdl )
* **Quake II** ( .md2 )
* **Quake III** ( .md3 
* **Quake 3 BSP** ( .pk3 )
* **RtCW** ( .mdc )
* **Doom 3** ( .md5mesh, .md5anim, .md5camera )
* **DirectX X** ( .x )
* **Quick3D** ( .q3o, .q3s )
* **Raw Triangles** ( .raw )
* **AC3D** ( .ac )
* **Stereolithography** ( .stl )
* **Autodesk DXF** ( .dxf )
* **Irrlicht Mesh** ( .irrmesh, .xml )
* **Irrlicht Scene** ( .irr, .xml )
* **Object File Format** ( .off )
* **Terragen Terrain** ( .ter )
* **3D GameStudio Model** ( .mdl )
* **3D GameStudio Terrain** ( .hmp )
* **Ogre** ( .mesh.xml, .skeleton.xml, .material )
* **Milkshape 3D** ( .ms3d )
* **LightWave Model** ( .lwo )
* **LightWave Scene** ( .lws )
* **Modo Model** ( .lxo )
* **CharacterStudio Motion** ( .csm )
* **Stanford Ply** ( .ply )
* **TrueSpace** ( .cob, .scn )

See the @link importer_notes Importer Notes Page @endlink for information, what a specific importer can do and what not.
Note that although this paper claims to be the official documentation,
https://github.com/assimp/assimp/blob/master/Readme.md
<br>is usually the most up-to-date list of file formats supported by the library. <br>

Assimp is independent of the Operating System by nature, providing a C++ interface for easy integration
with game engines and a C interface to allow bindings to other programming languages. At the moment the library runs
on any little-endian platform including X86/Windows/Linux/Mac and X64/Windows/Linux/Mac. Special attention
was paid to keep the library as free as possible from dependencies.

Big endian systems such as PPC-Macs or PPC-Linux systems are not officially supported at the moment. However, most
formats handle the required endian conversion correctly, so large parts of the library should work.

The assimp linker library and viewer application are provided under the BSD 3-clause license. This basically means
that you are free to use it in open- or closed-source projects, for commercial or non-commercial purposes as you like
as long as you retain the license information and take own responsibility for what you do with it. For details see
the LICENSE file.

You can find test models for almost all formats in the <assimp_root>/test/models directory. Beware, they're *free*,
but not all of them are *open-source*. If there's an accompagning '<file>\source.txt' file don't forget to read it.

.. _ai_main_install:

Installation
============

assimp can be used in two ways: linking against the pre-built libraries or building the library on your own. The former
option is the easiest, but the assimp distribution contains pre-built libraries only for Visual C++ 2013, 2015 and 2017. 
For other compilers you'll have to build assimp for yourself. Which is hopefully as hassle-free as the other way, but 
needs a bit more work. Both ways are described at the @link install Installation page. @endlink
If you want to use assimp on Ubuntu you can install it via the following command:

::

    sudo apt-get install assimp

If you want to use the python-assimp-port just follow these instructions: https://github.com/assimp/assimp/tree/master/port/PyAssimp

.. _ai_main_usage:

Usage
=====

When you're done integrating the library into your IDE / project, you can now start using it. There are two separate
interfaces by which you can access the library: a C++ interface and a C interface using flat functions. While the former
is easier to handle, the latter also forms a point where other programming languages can connect to. Up to the moment, though,
there are no bindings for any other language provided. Have a look at the @link usage Usage page @endlink for a detailed explanation and code examples.

.. _ai_main_data:

Data Structures
===============

When the importer successfully completed its job, the imported data is returned in an aiScene structure. This is the root
point from where you can access all the various data types that a scene/model file can possibly contain. The
@link data Data Structures page @endlink describes how to interpret this data.

.. _ai_ext:

Extending the library
=====================

There are many 3d file formats in the world, and we're happy to support as many as possible. If you need support for
a particular file format, why not implement it yourself and add it to the library? Writing importer plugins for
assimp is considerably easy, as the whole postprocessing infrastructure is available and does much of the work for you.
See the @link extend Extending the library @endlink page for more information.


.. _ai_main_support:

Support & Feedback
==================

If you have any questions/comments/suggestions/bug reports you're welcome to post them in our
<a href="https://sourceforge.net/forum/forum.php?forum_id=817653">forums</a>. Alternatively there's
a mailing list, <a href="https://sourceforge.net/mailarchive/forum.php?forum_name=assimp-discussions">
assimp-discussions</a>.


.. _ai_install_prebuilt:

Using the pre-built libraries with Visual C++ 8/9
=================================================

If you develop at Visual Studio 2015 or 2017, you can simply use the pre-built linker libraries provided in the distribution.
Extract all files to a place of your choice. A directory called "assimp" will be created there. Add the assimp/include path
to your include paths (Menu-&gt;Extras-&gt;Options-&gt;Projects and Solutions-&gt;VC++ Directories-&gt;Include files)
and the assimp/lib/&lt;Compiler&gt; path to your linker paths (Menu-&gt;Extras-&gt;Options-&gt;Projects and Solutions-&gt;VC++ Directories-&gt;Library files).
This is necessary only once to setup all paths inside you IDE.

To use the library in your C++ project you can simply generate a project file via cmake. One way is to add the assimp-folder 
as a subdirectory via the cmake-command

::

    addsubdiectory(assimp)

Now just add the assimp-dependency to your application:

::

    TARGET_LINK_LIBRARIES(my_game assimp)


If done correctly you should now be able to compile, link, run and use the application. 

.. _ai_install_own:

Building the library from scratch
=================================

First you need to install cmake. Now just get the code from github or download the latest version from the webside.
to build the library just open a command-prompt / bash, navigate into the repo-folder and run cmake via:

::

    cmake CMakeLists.txt

A project-file of your default make-system ( like gnu-make on linux or Visual-Studio on Windows ) will be generated. 
Run the build and you are done. You can find the libs at assimp/lib and the dll's / so's at bin.

.. _ai_assimp_dll:

Windows DLL Build
=================

The Assimp-package can be built as DLL. You just need to run the default cmake run.

.. _ai_static_lib:

Assimp static lib
=================

The Assimp-package can be build as a static library as well. Do do so just set the configuration variable <b>BUILD_SHARED_LIBS</b>
to off during the cmake run.
