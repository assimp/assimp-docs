.. image:: https://www.assimp.org/common/images/splash-color.png
.. _ai_introduction:

Introduction
------------

The **Asset-Importer-Lib** (in short **Assimp**, we will use this term for the library) is a library to load and process geometric scenes from various 3D-data formats. It 
is mostly tailored to typical game scenarios by supporting a node hierarchy, static or skinned meshes, materials, bone animations,
and potential texture data. But also some 3D-printing- and CAD-format are supported.
It is primarily useful for importing assets from various sources once and storing them in an intermediate format for easy and fast 
every-day-loading. The Asset-Importer-Lib is also able to apply various post-processing steps to the imported like:

* Model Validation
* Pretransforming
* Bounding-Box generation and more

The Assimp-Lib currently supports the following file formats:

* **3D Manufacturing Format** (.3mf)
* **Collada** (.dae, .xml)
* **Biovision BVH** (.bvh) 
* **3D Studio Max 3DS** (.3ds)
* **3D Studio Max ASE** (.ase)
* **glTF** (.glTF)
* **glTF2.0** (.glTF)

    * KHR_lights_punctual ( 5.0 )
    * KHR_materials_pbrSpecularGlossiness ( 5.0 )
    * KHR_materials_unlit ( 5.0 )
    * KHR_texture_transform ( 5.1 under test )
    
* **FBX-Format, as ASCII and binary** (.fbx)
* **Stanford Polygon Library** (.ply)
* **AutoCAD DXF** (.dxf)
* **IFC-STEP** (.ifc)
* **IQM-Format** (.iqm)
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

**Important:  Blender (.blend) support is deprecated.**
**To import a model from Blender, export the model from Blender to glTF.**
**Sorry for the inconvenience!**

See the:ref:`ai_importer_notes` for information, on what a specific importer can do and what not.
Note that although this paper claims to be the official documentation,
`README.md <https://github.com/assimp/assimp/blob/master/Readme.md>`_
is usually the most up-to-date list of file formats supported by the library.

Assimp is independent of the Operating System by nature, providing a C++ interface for easy integration
with game engines and a C-based interface to allow bindings to other programming languages. At the moment the library 
runs on any little-endian platform including **X86/Windows/Linux/Mac** and **X64/Windows/Linux/Mac**. Special attention
was paid to keeping the library as free as possible from dependencies.

Big-endian systems like PPC-based Macs (if you still have one) or PPC-Linux systems are supported as well.

The **Assimp** linker library and viewer application are provided under the BSD 3-clause license. This basically means
that you are free to use it in open- or closed-source projects, for commercial or non-commercial purposes as you like
as long as you retain the license information and take your own responsibility for what you do with it. For details see
the LICENSE file.

You can find test models for almost all formats in the **<assimp_root>/test/models** directory. Beware, they're *free*,
but not all of them are **open-source**. If there's an accompanying **'<file>\source.txt'** file don't forget to read it.

Dependencies
------------
The following libs are needed to compile the Asset-Importer-Lib. When checking out the code you don't have to take care 
about their installation. All of them are part of the repo or can be installed via Hunter.

* **zlib**
* **zip-lib**
* **unzip**
* **pugi-xml**
* **rapijson**
* **clipper**
* **draco**
* **gtest**
* **stb_image**
* **utf8cpp**
* **poly2tri**
* **openddlparser**
