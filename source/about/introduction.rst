.. image:: https://assimp.org/images/splash.png

.. _ai_introduction:

Introduction
------------

The Asset-Importer-Lib (in short assimp) is a library to load and process geometric scenes from various 3D-Dataformats. It 
is mostly tailored at typical game scenarios by supporting a node hierarchy, static or skinned meshes, materials, bone animations 
and potential texture data. But also some 3D-printing- and CAD-format are supported.
The library is *not* designed for speed, it is primarily useful for importing assets from various 
sources once and storing it in a engine-specific format for easy and fast every-day-loading. assimp is also able to apply 
various post processing steps to the imported data such as conversion to indexed meshes, calculation of normals or 
tangents/bitangents or conversion from right-handed to left-handed coordinate systems.

The Assimp-Lib currently supports the following file formats (note that some loaders lack some features of their formats because
some file formats contain data not supported by assimp, some stuff would require so much conversion work
that it has not been implemented yet and some (most ...) formats lack proper specifications):

* **3D Manufacturing Format** (.3mf)
* **Collada** (.dae, .xml)
* **Blender** (.blend)
* **Biovision BVH** (.bvh) 
* **3D Studio Max 3DS** (.3ds)
* **3D Studio Max ASE** (.ase)
* **glTF**(.glTF)
* ***glTF2.0** (.glTF)
  * KHR_lights_punctual ( 5.0 )
  * KHR_materials_pbrSpecularGlossiness ( 5.0 )
  * KHR_materials_unlit ( 5.0 )
  * KHR_texture_transform ( 5.1 under test )
* **FBX-Format, as ASCII and binary** (.fbx)
* **Stanford Polygon Library** (.ply)
* **AutoCAD DXF** (.dxf)
* **IFC-STEP** (.ifc)
* **Neutral File Format** (.nff)
* **Sense8 WorldToolkit** (.nff)
* **Valve Model** (.smd, .vta)
* **Quake I** (.mdl)
* **Quake II** (.md2)
* **Quake III** (.md3)
* **Quake 3 BSP** (.pk3)
* **RtCW** (.mdc)
* **Doom 3** (.md5mesh, .md5anim, .md5camera)
* **DirectX X** (.x)
* **Quick3D** (.q3o, .q3s)
* **Raw Triangles** (.raw)
* **AC3D** (.ac, .ac3d)
* **Stereolithography** (.stl)
* **Autodesk DXF** (.dxf)
* **Irrlicht Mesh** (.irrmesh, .xml)
* **Irrlicht Scene** (.irr, .xml)
* **Object File Format** ( .off )
* **Wavefront Object** (.obj) 
* **Terragen Terrain** ( .ter )
* **3D GameStudio Model** ( .mdl )
* **3D GameStudio Terrain** ( .hmp )
* **Ogre** ( .mesh.xml, .skeleton.xml, .material )
* **OpenGEX-Fomat** (.ogex)
* **Milkshape 3D** ( .ms3d )
* **LightWave Model** ( .lwo )
* **LightWave Scene** ( .lws )
* **Modo Model** ( .lxo )
* **CharacterStudio Motion** ( .csm )
* **Stanford Ply** ( .ply )
* **TrueSpace** (.cob, .scn)
* **XGL-3D-Format** (.xgl)

See the :ref:`ai_importer_notes` for information, what a specific importer can do and what not.
Note that although this paper claims to be the official documentation,
`README.md <https://github.com/assimp/assimp/blob/master/Readme.md>`_
is usually the most up-to-date list of file formats supported by the library.

Assimp is independent of the Operating System by nature, providing a C++ interface for easy integration
with game engines and a C-based interface to allow bindings to other programming languages. At the moment the library 
runs on any little-endian platform including **X86/Windows/Linux/Mac** and **X64/Windows/Linux/Mac**. Special attention
was paid to keep the library as free as possible from dependencies.

Big-endian systems like PPC-based Macs ( if you still have one) or PPC-Linux systems are supported as well.

The assimp linker library and viewer application are provided under the BSD 3-clause license. This basically means
that you are free to use it in open- or closed-source projects, for commercial or non-commercial purposes as you like
as long as you retain the license information and take own responsibility for what you do with it. For details see
the LICENSE file.

You can find test models for almost all formats in the **<assimp_root>/test/models** directory. Beware, they're *free*,
but not all of them are **open-source**. If there's an accompagning **'<file>\source.txt'** file don't forget to read it.

Dependencies
------------
The following libs are needed to compile the Asset-Importer-Lib. When checking out the code you don't have to take care 
about their installation. All of them are part of the repo or can be installed via Hunter.

* zlib
* zip-lib
* unzip
* pugi-xml
* rapijson
* clipper
* draco
* gtest
* stb_image
* utf8cpp
* poly2tri
* openddlparser
