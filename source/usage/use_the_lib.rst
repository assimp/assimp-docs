.. image:: https://www.assimp.org/common/images/splash-color.png
.. _ai_access_cpp:

===================================
Working with the Asset-Importer-Lib
===================================

Importing Data
==============

Access by C++ class interface
-----------------------------

The Asset-Importer-Lib can be accessed by both a class or flat function interface. The C++ class
the interface is the preferred way of interaction: you create an instance of the class Assimp::Importer,
maybe adjust some settings of it and then just call 
::

    Assimp::Importer::ReadFile(). 
    
The class will read the files and process its data, handing back the imported data as a pointer to an aiScene
to you. You can now extract the data you need from the file. The importer manages all the resources
for itself. If the importer is destroyed, all the data that was created/read by it will be
destroyed, too. So the easiest way to use the Importer is to create an instance locally, use its
results and then simply let it go out of scope.

*C++ example:*

::

    #include <assimp/Importer.hpp>      // C++ importer interface
    #include <assimp/scene.h>           // Output data structure
    #include <assimp/postprocess.h>     // Post processing flags

    bool DoTheImportThing( const std::string& pFile) {
      // Create an instance of the Importer class
      Assimp::Importer importer;

      // And have it read the given file with some example postprocessing
      // Usually - if speed is not the most important aspect for you - you'll
      // probably to request more postprocessing than we do in this example.
      const aiScene* scene = importer.ReadFile( pFile,
        aiProcess_CalcTangentSpace       |
        aiProcess_Triangulate            |
        aiProcess_JoinIdenticalVertices  |
        aiProcess_SortByPType);

      // If the import failed, report it
      if (nullptr == scene) {
        DoTheErrorLogging( importer.GetErrorString());
        return false;
      }

      // Now we can access the file's contents.
      DoTheSceneProcessing( scene);

      // We're done. Everything will be cleaned up by the importer destructor
      return true;
    }

What exactly is read from the files and how you interpret it is described at the:ref:`ai_data`.
The post-processing steps that the Assimp library can apply to the
imported data are listed at #aiPostProcessSteps. See the @ref pp Post processing page for more details.

Note that the **aiScene** data structure returned is declared 'const'. Yes, you can get rid of
these 5 letters with a simple cast. Yes, you may do that. No, it's not recommended (and it's
suicide in DLL builds if you try to use new or delete on any of the arrays in the scene).

.. _ai_access_c:

Access by plain-c function interface
------------------------------------

The plain function interface is just as simple but requires you to manually call the clean-up
after you're done with the imported data. To start the import process, call **aiImportFile()**
with the filename in question and the desired postprocessing flags like above. If the call
is successful, an aiScene pointer with the imported data is handed back to you. When you're
done with the extraction of the data you're interested in, call **aiReleaseImport()** on the
imported scene to clean up all resources associated with the import.

*C-Example:*

::

    #include <assimp/cimport.h>        // Plain-C interface
    #include <assimp/scene.h>          // Output data structure
    #include <assimp/postprocess.h>    // Post processing flags

    bool DoTheImportThing( const char* pFile) {
      // Start the import on the given file with some example postprocessing
      // Usually - if speed is not the most important aspect for you - you'll t
      // probably to request more postprocessing than we do in this example.
      const struct aiScene* scene = aiImportFile( pFile,
        aiProcess_CalcTangentSpace       |
        aiProcess_Triangulate            |
        aiProcess_JoinIdenticalVertices  |
        aiProcess_SortByPType);

      // If the import failed, report it
      if( NULL == scene) {
        DoTheErrorLogging( aiGetErrorString());
        return false;
      }

      // Now we can access the file's contents
      DoTheSceneProcessing( scene);

      // We're done. Release all resources associated with this import
      aiReleaseImport( scene);
      return true;
    }

.. _ai_custom_io:

Using custom IO logic with the C++ class interface
--------------------------------------------------

The Assimp library needs to access files internally. This of course applies to the file you want
to read, but also to additional files in the same folder for certain file formats. By default,
standard C/C++ IO logic is used to access these files. If your application works in a special
environment where custom logic is needed to access the specified files, you have to supply
custom implementations of IOStream and IOSystem. A shortened example might look like this:

::

    #include <assimp/IOStream.hpp>
    #include <assimp/IOSystem.hpp>

    // My own implementation of IOStream
    class MyIOStream : public Assimp::IOStream {
      friend class MyIOSystem;

    protected:
      // Constructor protected for private usage by MyIOSystem
      MyIOStream();

    public:
      ~MyIOStream();
      size_t Read( void* pvBuffer, size_t pSize, size_t pCount) { ... }
      size_t Write( const void* pvBuffer, size_t pSize, size_t pCount) { ... }
      aiReturn Seek( size_t pOffset, aiOrigin pOrigin) { ... }
      size_t Tell() const { ... }
      size_t FileSize() const { ... }
      void Flush () { ... }
    };

    // Fisher Price - My First Filesystem
    class MyIOSystem : public Assimp::IOSystem {
      MyIOSystem() { ... }
      ~MyIOSystem() { ... }

      // Check whether a specific file exists
      bool Exists( const std::string& pFile) const {
        ..
      }

      // Get the path delimiter character we'd like to see
      char GetOsSeparator() const {
        return '/';
      }

      // ... and finally a method to open a custom stream
      IOStream* Open( const std::string& pFile, const std::string& pMode) {
        return new MyIOStream( ... );
      }

      void Close( IOStream* pFile) { delete pFile; }
    };

Now that your IO system is implemented, supply an instance of it to the Importer object by calling
::

    Assimp::Importer::SetIOHandler().

An example:

::

    void DoTheImportThing( const std::string& pFile) {
      Assimp::Importer importer;
      // put my custom IO handling in place
      importer.SetIOHandler( new MyIOSystem());

      // the import process will now use this implementation to access any file
      importer.ReadFile( pFile, SomeFlag | SomeOtherFlag);
    }

.. _ai_custom_io_c:

Using custom IO logic with the plain-c function interface
---------------------------------------------------------

The C interface also provides a way to override the file system. Control is not as fine-grained as for C++ although
surely enough for almost any purpose. The process is simple:


* Include cfileio.h
* Fill an aiFileIO structure with custom file system callbacks (they're self-explanatory as they work similarly to the CRT's fXXX functions)
* and pass it as a parameter to #aiImportFileEx

.. _ai_logging:

Logging
-------

The Assimp-library provides an easy mechanism to log messages. For instance, if you want to check the state of your
import and you just want to see, after which preprocessing step the import process was aborted you can take a look
into the log.
Per default, the Assimp-library provides a default log implementation, where you can log your user-specific message
by calling it a singleton with the requested logging type. To see how this works take a look at this:

::

    using namespace Assimp;

    // Create a logger instance
    DefaultLogger::create("", Logger::VERBOSE);

    // Now I am ready for logging my stuff
    DefaultLogger::get()->info("this is my info-call");

    // Kill it after the work is done
    DefaultLogger::kill();

At first, you have to create the default-logger-instance (create). Now you are ready to rock and can log a
little bit around. After that, you should kill it to release the singleton instance.

If you want to integrate the assimp-log into your own GUI it may be helpful to have a mechanism writing
the logs into your own log windows. The logger interface provides this by implementing an interface called **LogStream**.
You can attach and detach this log stream to the default-logger instance or any implementation derived from Logger.
Just derivate your own logger from the abstract base-class **LogStream** and overwrite the write method:

::

    // Example stream
    class myStream : public LogStream {
    public:
        // Write something using your own functionality
        void write(const char* message) {
            ::printf("%s\n", message);
        }
    };

    // Select the kinds of messages you want to receive on this log stream
    const unsigned int severity = Logger::Debugging|Logger::Info|Logger::Err|Logger::Warn;

    // Attaching it to the default logger
    Assimp::DefaultLogger::get()->attachStream( new myStream, severity );

The severity level controls the kind of message which will be written into
the attached stream. If you just want to log errors and warnings set the warn
and error severity flag for those severities. It is also possible to remove
a self-defined log stream from an error severity by detaching it with the severity
flag set:

::

    unsigned int severity = 0;
    severity |= Logger::Debugging;

    // Detach debug messages from your self defined stream
    Assimp::DefaultLogger::get()->attachStream( new myStream, severity );


If you want to implement your own logger just derive from the abstract base class
**Logger** and overwrite the methods debug, info, warn, and error.

If you want to see the debug messages in a debug-configured build, the Logger-interface
provides a logging severity. You can set it by calling the following method:

::

    Assimp::DefaultLogger::get()->setLogSeverity( LogSeverity log_severity );


The normal logging severity supports just the basic stuff like info, warnings, and errors.
In the verbose level very fine-grained debug messages will be logged, too. Note that this
kind of logging might decrease import performance.

.. _ai_data:

Exporting models
================

A valid **aiScene** instance can be used to export into a requested assset-format.

For instance:

::

    bool exporterTest() override {
        ::Assimp::Importer importer;
        ::Assimp::Exporter exporter;
        const aiScene *scene = importer.ReadFile(ASSIMP_TEST_MODELS_DIR "/OBJ/spider.obj", aiProcess_ValidateDataStructure);
        exporter.Export(scene, "obj", ASSIMP_TEST_MODELS_DIR "/OBJ/spider_out.obj");
        return true;
    }

The following file formats are currently supported:

* collada
* x
* stp
* obj
* objnomtl
* stl
* stlb
* ply
* plyb
* 3ds
* gltf2
* glb2
* gltf
* glb
* assbin
* assxml
* x3d
* fbx
* fbxa
* m3da
* 3mf
* pbrt
* assjson

Data Structures
===============

Introduction
------------

The Assimp-Library returns the imported data in a collection of structures. **aiScene** forms the root
of the data, from here you gain access to all the nodes, meshes, materials, animations, or textures
that was read from the imported file. The **aiScene** is returned from a successful call to
**Assimp::Importer::ReadFile()**, **aiImportFile()** or **aiImportFileEx()** - see the :ref:`ai_usage`
for further information on how to use the library.

By default, all 3D data is provided in a right-handed coordinate system such as OpenGL uses. In
this coordinate system, +X points to the right, +Y points upwards and +Z points out of the screen
towards the viewer. Several modeling packages such as 3D Studio Max use this coordinate system as well
(or a rotated variant of it).
By contrast, some other environments use left-handed coordinate systems, a prominent example being
DirectX. If you need the imported data to be in a left-handed coordinate system, supply the
#aiProcess_MakeLeftHanded flag to the **ReadFile()** function call.

The output face winding is counterclockwise. Use #aiProcess_FlipWindingOrder to get CW data.

::

    x2

                x1
        x0

Outputted polygons can be literally everything: they're probably concave, self-intersecting or non-planar,
although our built-in triangulation (#aiProcess_Triangulate postprocessing step) doesn't handle the two latter.

The output UV coordinate system has its origin in the lower-left corner:

::

    0x|1y ---------- 1x|1y
     |                |
     |                |
     |                |
    0x|0y ---------- 1x|0y

Use the #aiProcess_FlipUVs flag to get UV coordinates with the upper-left corner as origin.

A typical 4x4 matrix including a translational part looks like this:

::

    X1  Y1  Z1  T1
    X2  Y2  Z2  T2
    X3  Y3  Z3  T3
     0   0   0   1

with <tt>(X1, X2, X3)</tt> being the local X base vector, <tt>(Y1, Y2, Y3)</tt> being the local
Y base vector, <tt>(Z1, Z2, Z3)</tt> being the local Z base vector and <tt>(T1, T2, T3)</tt> being the
offset of the local origin (the translational part). 
All matrices in the library use row-major storage order. That means that the matrix elements are
stored row-by-row, i.e. they end up like this in memory: 
<tt>[X1, Y1, Z1, T1, X2, Y2, Z2, T2, X3, Y3, Z3, T3, 0, 0, 0, 1]</tt>. 

Note that this is neither the OpenGL format nor the DirectX format, because both of them specify the
matrix layout such that the translational part occupies three consecutive addresses in memory (so those
matrices end with <tt>[..., T1, T2, T3, 1]</tt>), whereas the translation in an Assimp matrix is found at
the offsets 3, 7 and 11 (spread across the matrix). You can transpose an Assimp matrix to end up with
the format that OpenGL and DirectX mandate. To be very precise: The transposition has nothing
to do with a left-handed or right-handed coordinate system but 'converts' between row-major and
column-major storage formats.

<b>11.24.09:</b> We changed the orientation of our quaternions to the most common convention to avoid confusion.
However, if you're a previous user of Assimp and you update the library to revisions beyond SVNREV 502,
you have to adapt your animation loading code to match the new quaternion orientation.

.. _ai_hierarchy:

The Node-Hierarchy
------------------

Nodes are little-named entities in the scene that have a place and orientation relative to their parents.
Starting from the scene's root node all nodes can have 0 to x child nodes, thus forming a hierarchy.
They form the base on which the scene is built: a node can refer to 0..x meshes, can be referred to
by a bone of a mesh, or can be animated by a key sequence of animation. DirectX calls them "frames",
others call them "objects", and we call them **aiNode**.

A node can potentially refer to single or multiple meshes. The meshes are not stored inside the node, but
instead in an array of **aiMesh** inside the aiScene. A node only refers to them by their array index. This also means
that multiple nodes can refer to the same mesh, which provides a simple form of instancing. A mesh referred to
in this way lives in the node's local coordinate system. If you want the mesh's orientation in global
space, you'd have to concatenate the transformations from the referring node and all of its parents.

Most of the file formats don't really support complex scenes, though, but a single model only. But there are
more complex formats such as .3ds, .x, or .collada scenes which may contain an arbitrarily complex
hierarchy of nodes and meshes. I myself would suggest a recursive filter function such as the
following pseudocode:

::

	void CopyNodesWithMeshes( aiNode node, SceneObject targetParent, Matrix4x4 accTransform) {
	  SceneObject parent;
	  Matrix4x4 transform;

	  //If node has meshes, create a new scene object for it
	  if( node.mNumMeshes > 0) {
		SceneObject newObject = new SceneObject;
		targetParent.addChild( newObject);
		// copy the meshes
		CopyMeshes( node, newObject);

		//The new object is the parent for all child nodes
		parent = newObject;
		transform.SetUnity();
	  } else {
		// if no meshes, skip the node, but keep its transformation
		parent = targetParent;
		transform = node.mTransformation * accTransform;
	  }

	  // continue for all child nodes
	  for( all node.mChildren) {
		CopyNodesWithMeshes( node.mChildren[a], parent, transform);
          }
	}
	
This function copies a node into the scene graph if it has children. If yes, a new scene object
is created for the import node and the node's meshes are copied over. If not, no object is created.
Potential child objects will be added to the old targetParent, but their transformation will be correct
in respect to the global space. This function also works great in filtering the bone nodes - nodes
that form the bone hierarchy for another mesh/node, but don't have any mesh themselves.

.. _ai_meshes:

Meshes
------

All meshes of an imported scene are stored in an array of aiMesh* inside the aiScene. Nodes refer
to them by their index in the array and provide the coordinate system for them, too. One mesh uses
only a single material everywhere - if parts of the model use a different material, this part is
moved to a separate mesh at the same node. The mesh refers to its material in the same way as the
node refers to its meshes: materials are stored in an array inside **aiScene**, and the mesh stores only
an index into this array.

An **aiMesh** is defined by a series of data channels. The presence of these data channels is defined
by the contents of the imported file: by default, there are only those data channels present in the mesh
that were also found in the file. The only channels guaranteed to be always present are aiMesh::mVertices
and aiMesh::mFaces. You can test for the presence of other data by testing the pointers against NULL
or using the helper functions provided by **aiMesh**. You may also specify several post-processing flags
at Importer::ReadFile() to let Assimp calculate or recalculate additional data channels for you.

At the moment, a single aiMesh may contain a set of triangles and polygons. A single vertex does always
have a position. In addition, it may have one normal, one tangent, and bitangent, zero to **AI_MAX_NUMBER_OF_TEXTURECOORDS**
(4 at the moment) texture coords and zero to AI_MAX_NUMBER_OF_COLOR_SETS (4) vertex colors. In addition,
a mesh may or may not have a set of bones described by an array of **aiBone** structures. How to interpret
the bone information is described later on.

.. _ai_material:

Materials
---------

See the:ref:`ai_material` Material System Page.


.. _ai_textures:

Textures
--------

Normally textures used by assets are stored in separate files, however,
there are file formats embedding their textures directly into the model file.
Such textures are loaded into an **aiTexture** structure.

In previous versions, the path from the query for `AI_MATKEY_TEXTURE(textureType, index)` would be
`*<index>` where `<index>` is the index of the texture in aiScene::mTextures. Now this call will
return a file path for embedded textures in FBX files. To test if it is an embedded texture use
aiScene::GetEmbeddedTexture. If the returned pointer is not null, it is embedded and can be loaded
from the data structure. If it is null, search for a separate file. Other file types still use the
old behavior.

If you rely on the old behavior, you can use Assimp::Importer::SetPropertyBool with the key
#AI_CONFIG_IMPORT_FBX_EMBEDDED_TEXTURES_LEGACY_NAMING to force the old behavior.

There are two cases:
 * The texture is NOT compressed. Its color data is directly stored in the **aiTexture** structure as an array of 
   aiTexture::mWidth * aiTexture::mHeight 
   **aiTexel** structures. Each **aiTexel** represents a
   pixel (or "texel") of the texture image. The color data is stored in an unsigned RGBA8888 format,
   which can be easily used for both Direct3D and OpenGL (swizzling the order of the color
   components might be necessary).  RGBA8888 has been chosen because it is well-known, easy to use
   , and natively supported by nearly all graphics APIs.
 * This applies if aiTexture::mHeight == 0 is fulfilled. Then, the texture is stored in a compressed
   format such as DDS or PNG. The term "compressed" does not mean that the texture data must
   actually be compressed, however, the texture was found in the model file as if it was stored in a
   separate file on the hard disk. Appropriate decoders (such as libjpeg, libpng, D3DX, DevIL) are
   required to load these textures.  aiTexture::mWidth specifies the size of the texture data in
   bytes, aiTexture::pcData is a pointer to the raw image data and aiTexture::achFormatHint is
   either zeroed or contains the most common file extension of the embedded texture's format. This
   value is only set if Assimp is able to determine the file format.
   
.. _ai_materials:

Material-System
===============

General Overview
################################

All materials are stored in an array of **aiMaterial** inside the aiScene.

Each aiMesh refers to one
material by its index in the array. Due to the vastly diverging definitions and usages of material
parameters, there is no hard definition of a material structure. Instead, a material is defined by
a set of properties accessible by their names. Have a look at assimp/material.h to see what types of
properties are defined. In this file, there are also various functions defined to test for the
presence of certain properties in a material and retrieve their values.

.. _ai_mat_tex:

Textures
--------

Textures are organized in stacks, each stack being evaluated independently. The final color value from a particular texture stack is used in the shading equation. 
For example, the computed color value of the diffuse texture stack (aiTextureType_DIFFUSE) is multiplied with the amount of incoming diffuse light to obtain the 
final diffuse color of a pixel.

.. list-table::
	:widths: auto
	:header-rows: 1
	
	* - Stack
	  - Resulting equation
	  
	* - Constant base color
	  - color
	  
	* - Blend operation 0
	  - +
	  
	* - Strength factor 0
	  - 0.25*
	  
	* - Texture 0
	  - texture_0
	  
	* - Blend operation 1
	  - x
	  
	* - Strength factor 1
	  - 1.0*
	  
	* - Texture 1
	  - texture_1

	  
.. _ai_keys:

Constants
---------

All material key constants start with 'AI_MATKEY' as a prefix.

.. list-table::
	:widths: auto
	:header-rows: 1

	* - Name
	  - Data Type
	  - Default Value
	  - Meaning
	  - Notes
	  
	* - NAME
	  - aiString
	  - n/a
	  - The name of the material, if available.
	  - Ignored by <tt>aiProcess_RemoveRedundantMaterials. Materials are considered equal even if their names are different.

	* - COLOR_DIFFUSE
	  - aiColor3D
	  - black (0,0,0)
	  - Diffuse color of the material. This is typically scaled by the amount of incoming diffuse light (e.g. using gouraud shading)
	  - n/a

	* - COLOR_SPECULAR
	  - aiColor3D
	  - black (0,0,0)
	  - Specular color of the material. This is typically scaled by the amount of incoming specular light (e.g. using phong shading)
	  - n/a

	* - COLOR_AMBIENT
	  - aiColor3D
	  - black (0,0,0)
	  - Ambient color of the material. This is typically scaled by the amount of ambient light
	  - n/a

	* - COLOR_EMISSIVE
	  - aiColor3D
	  - black (0,0,0)
	  - Emissive color of the material. This is the amount of light emitted by the object. In real time applications it will usually not affect surrounding objects, but raytracing applications may wish to treat emissive objects as light sources.
	  - n/a

	* - COLOR_TRANSPARENT
	  - aiColor3D
	  - black (0,0,0)
	  - Defines the transparent color of the material, this is the color to be multiplied with the color of translucent light to construct the final 'destination color' for a particular position in the screen buffer.
	  - n/a

	* - COLOR_REFLECTIVE
	  - aiColor3D
	  - <td>black (0,0,0)
	  - Defines the reflective color of the material. This is typically scaled by the amount of incoming light from the direction of mirror reflection. Usually combined with an environment lightmap of some kind for real-time applications.
	  - n/a

	* - REFLECTIVITY
	  - float
	  - 0.0
	  - Scales the reflective color of the material.
	  - n/a

	* - WIREFRAME
	  - int
	  - false
	  - Specifies whether wireframe rendering must be turned on for the material. 0 for false, !0 for true.
	  - n/a

	* - TWOSIDED
	  - int
	  - false
	  - Specifies whether meshes using this material must be rendered without backface culling. 0 for false, !0 for true.
	  - Some importers set this property if they don't know whether the output face order is right. As long as it is not set, you may safely enable backface culling.

	* - SHADING_MODEL
	  - int
	  - gouraud
	  - One of the #aiShadingMode enumerated values. Defines the library shading model to use for (real time) rendering to approximate the original look of the material as closely as possible.
	  - The presence of this key might indicate a more complex material. If absent, assume phong shading only if a specular exponent is given.

	* - BLEND_FUNC
	  - int
	  - false
	  - One of the #aiBlendMode enumerated values. Defines how the final color value in the screen buffer is computed from the given color at that position and the newly computed color from the material. Simply said, alpha blending settings.
	  - n/a

	* - OPACITY
	  - float
	  - 1.0
	  - Defines the opacity of the material in a range between 0..1.
	  - Use this value to decide whether you have to activate alpha blending for rendering. **OPACITY!=1** usually also implies **TWOSIDED=1** to avoid cull artifacts.

	* - SHININESS
	  - float
	  - 0.f
	  - Defines the shininess of a phong-shaded material. This is actually the exponent of the phong specular equation
	  - **SHININESS=0** is equivalent to **SHADING_MODEL = aiShadingMode_Gouraud**

	* - SHININESS_STRENGTH
	  - float
	  - 1.0
	  - Scales the specular color of the material.
	  - This value is kept separate from the specular color by most modelers, and so do we.

	* - REFRACTI
	  - float
	  - 1.0
	  - Defines the Index Of Refraction for the material. That's not supported by most file formats.
	  - Might be of interest for raytracing.

	* - TEXTURE(t,n)
	  - aiString
	  - n/a
	  - Defines the path of the n'th texture on the stack 't', where 'n' is any value >= 0 and 't' is one of the #aiTextureType enumerated values. A file path to an external file or an embedded texture. Use aiScene::GetEmbeddedTexture to test if it is embedded for FBX files, in other cases embedded textures start with '*' followed by an index into aiScene::mTextures.
	  - See the @ref mat_tex section above. Also see @ref textures for a more information about texture retrieval.

	* - TEXBLEND(t,n)
	  - float</td>
	  - n/a
	  - Defines the strength the n'th texture on the stack 't'. All color components (rgb) are multiplied with this factor *before* any further processing is done.
	  - n/a

	* - TEXOP(t,n)
	  - int
	  - n/a
	  - One of the #aiTextureOp enumerated values. Defines the arithmetic operation to be used to combine the n'th texture on the stack 't' 
	    with the n-1'th. **TEXOP(t,0)** refers to the blend operation between the base color for this stack (e.g. **COLOR_DIFFUSE** for the diffuse stack) 
	    and the first texture.
	  - n/a

	* - MAPPING(t,n)
	  - int
	  - n/a
	  - Defines how the input mapping coordinates for sampling the n'th texture on the stack 't' are computed. Usually explicit UV coordinates are provided, 
	    but some model file formats might also be using basic shapes, such as spheres or cylinders, to project textures onto meshes.
	  - See the 'Textures' section below. #aiProcess_GenUVCoords can be used to let Assimp compute proper UV coordinates from projective mappings.

	* - UVWSRC(t,n)
	  - int
	  - n/a
	  - Defines the UV channel to be used as input mapping coordinates for sampling the n'th texture on the stack 't'. All meshes assigned to this material 
	    share the same UV channel setup
	  - Presence of this key implies **MAPPING(t,n)** to be #aiTextureMapping_UV. See @ref uvwsrc for more details.

	* - MAPPINGMODE_U(t,n)
	  - int
	  - n/a
	  - Any of the #aiTextureMapMode enumerated values. Defines the texture wrapping mode on the x axis for sampling the n'th texture on the stack 't'. 
	    'Wrapping' occurs whenever UVs lie outside the **0..1** range.
	  - n/a

	* - MAPPINGMODE_V(t,n)
	  - int
	  - n/a
	  - Wrap mode on the v axis. See *MAPPINGMODE_U*.
	  - n/a

	* - TEXMAP_AXIS(t,n)
	  - aiVector3D
	  - n/a
	  - Defines the base axis to to compute the mapping coordinates for the n'th texture on the stack 't' from. This is not required for UV-mapped textures. 
	    For instance, if <tt>MAPPING(t,n)</tt> is #aiTextureMapping_SPHERE, U and V would map to longitude and latitude of a sphere around the given axis. 
	    The axis is given in local mesh space.
	  - n/a

	* - TEXFLAGS(t,n)
	  - int
	  - n/a
	  - Defines miscellaneous flag for the n'th texture on the stack 't'. This is a bitwise combination of the #aiTextureFlags enumerated values.
	  - n/a

.. _ai_cpp:

C++-API
-------

Retrieving a property from a material is done using various utility functions. For C++ it's simply calling aiMaterial::Get()

::

	aiMaterial* mat = .....
	
	// The generic way
	if(AI_SUCCESS != mat->Get(<material-key>,<where-to-store>)) {
	   // handle epic failure here
	}

Simple, isn't it? To get the name of a material you would use

::

	aiString name;
	mat->Get(AI_MATKEY_NAME,name);

Or for the diffuse color ('color' won't be modified if the property is not set)

::

	aiColor3D color (0.f,0.f,0.f);
	mat->Get(AI_MATKEY_COLOR_DIFFUSE,color);

<b>Note:</b> Get() is actually a template with explicit specializations for aiColor3D, aiColor4D, aiString, float, int and some others.
Make sure that the type of the second parameter matches the expected data type of the material property (no compile-time check yet!).
Don't follow this advice if you wish to encounter very strange results.

.. _ai_c:

C-API
-----

For good old C it's slightly different. Take a look at the aiGetMaterialGet<data-type> functions.

::

	aiMaterial* mat = .....
	
	if(AI_SUCCESS != aiGetMaterialFloat(mat,<material-key>,<where-to-store>)) {
	   // handle epic failure here
	}

To get the name of a material you would use

::

	aiString name;
	aiGetMaterialString(mat,AI_MATKEY_NAME,&name);

Or for the diffuse color ('color' won't be modified if the property is not set)

::

	aiColor3D color (0.f,0.f,0.f);
	aiGetMaterialColor(mat,AI_MATKEY_COLOR_DIFFUSE,&color);

.. _ai_uvsrc:
   
How to map UV channels to textures (MATKEY_UVWSRC)
--------------------------------------------------

The MATKEY_UVWSRC property is only present if the source format doesn't specify an explicit mapping from
textures to UV channels. Many formats don't do this and assimp is not aware of a perfect rule either.

Your handling of UV channels needs to be flexible therefore. Our recommendation is to use logic like this
to handle most cases properly:

::
	have only one uv channel?
	   assign channel 0 to all textures and break

	for all textures
	   have uvwsrc for this texture?
	      assign channel specified in uvwsrc
	   else
	      assign channels in ascending order for all texture stacks,
	      i.e. diffuse1 gets channel 1, opacity0 gets channel 0.

.. _ai_pseudo:

Pseudo Code Listing
######################################

For completeness, the following is a very rough pseudo-code sample showing how to evaluate Assimp materials in your
shading pipeline. You'll probably want to limit your handling of all those material keys to a reasonable subset suitable for your purposes
(for example most 3d engines won't support highly complex multi-layer materials, but many 3d modellers do).

Also note that this sample is targeted at a (shader-based) rendering pipeline for real-time graphics.

::

	// ---------------------------------------------------------------------------------------
	// Evaluate multiple textures stacked on top of each other
	float3 EvaluateStack(stack) {
          // For the 'diffuse' stack.base_color would be COLOR_DIFFUSE
	  // and TEXTURE(aiTextureType_DIFFUSE,n) the n'th texture.

	  float3 base = stack.base_color;
	  for (every texture in the stack) {
	    // assuming we have explicit & pre transformed UVs for this texture
	    float3 color = SampleTexture(texture,uv);
	
	    // scale by texture blend factor
	    color *= texture.blend;
	
	    if (texture.op == add)
	      base += color;
	    else if (texture.op == multiply)
	      base *= color;
	    else // other blend ops go here
	  }
	  return base;
	}
	
	// ---------------------------------------------------------------------------------------
	// Compute the diffuse contribution for a pixel
	float3 ComputeDiffuseContribution() {
	  if (shading == none)
	     return float3(1,1,1);

	  float3 intensity (0,0,0);
	  for (all lights in range) {
	    float fac = 1.f;
	    if (shading == gouraud)
	      fac =  lambert-term ..
	    else // other shading modes go here
	
	    // handling of different types of lights, such as point or spot lights
	    // ...

	    // and finally sum the contribution of this single light ...
	    intensity += light.diffuse_color * fac;
	  }
	  // ... and combine the final incoming light with the diffuse color
	  return EvaluateStack(diffuse) * intensity;
	}
	
	// ---------------------------------------------------------------------------------------
	// Compute the specular contribution for a pixel
	float3 ComputeSpecularContribution() {
	  if (shading == gouraud || specular_strength == 0 || specular_exponent == 0)
	    return float3(0,0,0);

	  float3 intensity (0,0,0);
	  for (all lights in range) {
	    float fac = 1.f;
	    if (shading == phong)
	      fac =  phong-term ..
	    else // other specular shading modes go here
	
	    // handling of different types of lights, such as point or spot lights
	    // ...

	    // and finally sum the specular contribution of this single light ...
	    intensity += light.specular_color * fac;
	  }
	  // ... and combine the final specular light with the specular color
	  return EvaluateStack(specular) * intensity * specular_strength;
	}
	
	// ---------------------------------------------------------------------------------------
	// Compute the ambient contribution for a pixel
	float3 ComputeAmbientContribution() {
	  if (shading == none)
	     return float3(0,0,0);
	
	  float3 intensity (0,0,0);
	  for (all lights in range) {
	    float fac = 1.f;
	
	    // handling of different types of lights, such as point or spot lights
	    // ...
	
	    // and finally sum the ambient contribution of this single light ...
	    intensity += light.ambient_color * fac;
	  }
	  // ... and combine the final ambient light with the ambient color
	  return EvaluateStack(ambient) * intensity;
	}
	
	// ---------------------------------------------------------------------------------------
	// Compute the final color value for a pixel
	// @param prev Previous color at that position in the framebuffer
	float4 PimpMyPixel (float4 prev) {
	  // .. handle displacement mapping per vertex
	  // .. handle bump/normal mapping
	
	  // Get all single light contribution terms
	  float3 diff = ComputeDiffuseContribution();
	  float3 spec = ComputeSpecularContribution();
	  float3 ambi = ComputeAmbientContribution();

	  // .. and compute the final color value for this pixel
	  float3 color = diff + spec + ambi;
	  float3 opac  = EvaluateStack(opacity);
	
	  // note the *slightly* strange meaning of additive and multiplicative blending here ...
	  // those names will most likely be changed in future versions
	  if (blend_func == add)
	       return prev+color*opac;
	  else if (blend_func == multiply)
	       return prev*(1.0-opac)+prev*opac;

	   return color;
	}

.. _ai_shdacc:

How to access shader-code
-------------------------
You can get the shadercode like a texture (AI_MATKEY_GLOBAL_SHADERLANG and AI_MATKEY_SHADER_VERTEX, ...)
You can get assigned shader sources by using the following material keys:

* *AI_MATKEY_GLOBAL_SHADERLANG*  To get the used shader language.
* *AI_MATKEY_SHADER_VERTEX*      Assigned vertex shader code stored as a string.
* *AI_MATKEY_SHADER_FRAGMENT*    Assigned fragment shader code stored as a string.
* *AI_MATKEY_SHADER_GEO*         Assigned geometry shader code stored as a string.
* *AI_MATKEY_SHADER_TESSELATION* Assigned tesselation shader code stored as a string.
* *AI_MATKEY_SHADER_PRIMITIVE*   Assigned primitive shader code stored as a string.
* *AI_MATKEY_SHADER_COMPUTE*     Assigned compute shader code stored as a string.

.. _ai_AnimationOverview:

Animation Overview
==================

<a href="http://ogldev.atspace.co.uk/www/tutorial38/tutorial38.html">This external tutorial</a>
has working code to get started implementing animations using bone matrix array in the vertex shader.
(If using **glm** (OpenGL math library), cross-reference with <a href="http://www.xphere.me/2019/05/bones-animation-with-openglassimpglm/">this page</a>
which has useful tips on converting between **Assimp** and **glm** objects)

.. _ai_Transformations:

Transformations
---------------

 This diagram shows how you can calculate your transformation matrices for an animated character:
 .. image:: ../images/AnimationOverview.png
 

.. _ai_perf:

Performance
===========

.. _ai_perf_overview:

Overview
--------

This page discusses general performance issues related to **Assimp**.

.. _ai_perf_profile:

Profiling
---------

Assimp has built-in support for <i>very</i> basic profiling and time measurement. To turn it on, set the <tt>GLOB_MEASURE_TIME</tt>
configuration switch to <tt>true</tt> (nonzero). Results are dumped to the log file, so you need to set up
an appropriate logger implementation with at least one output stream first (see the @:ref:`ai_logging` for the details.).

Note that these measurements are based on a single run of the importer and each of the post-processing steps, so
a single result set is far away from being significant in a statistical sense. While precision can be improved
by running the test multiple times, the low accuracy of the timings may render the results useless
for smaller files.

A sample report looks like this (some unrelated log messages omitted, entries grouped for clarity):

::

	Debug, T5488: START `total`
	Info,  T5488: Found a matching importer for this file format
	
	
	Debug, T5488: START `import`
	Info,  T5488: BlendModifier: Applied the `Subdivision` modifier to `OBMonkey`
	Debug, T5488: END   `import`, dt= 3.516 s
	
	
	Debug, T5488: START `preprocess`
	Debug, T5488: END   `preprocess`, dt= 0.001 s
	Info,  T5488: Entering post processing pipeline
	
	
	Debug, T5488: START `postprocess`
	Debug, T5488: RemoveRedundantMatsProcess begin
	Debug, T5488: RemoveRedundantMatsProcess finished
	Debug, T5488: END   `postprocess`, dt= 0.001 s
	
	
	Debug, T5488: START `postprocess`
	Debug, T5488: TriangulateProcess begin
	Info,  T5488: TriangulateProcess finished. All polygons have been triangulated.
	Debug, T5488: END   `postprocess`, dt= 3.415 s
	
	
	Debug, T5488: START `postprocess`
	Debug, T5488: SortByPTypeProcess begin
	Info,  T5488: Points: 0, Lines: 0, Triangles: 1, Polygons: 0 (Meshes, X = removed)
	Debug, T5488: SortByPTypeProcess finished
	
	Debug, T5488: START `postprocess`
	Debug, T5488: JoinVerticesProcess begin
	Debug, T5488: Mesh 0 (unnamed) | Verts in: 503808 out: 126345 | ~74.922
	Info,  T5488: JoinVerticesProcess finished | Verts in: 503808 out: 126345 | ~74.9
	Debug, T5488: END   `postprocess`, dt= 2.052 s
	
	Debug, T5488: START `postprocess`
	Debug, T5488: FlipWindingOrderProcess begin
	Debug, T5488: FlipWindingOrderProcess finished
	Debug, T5488: END   `postprocess`, dt= 0.006 s
	
	
	Debug, T5488: START `postprocess`
	Debug, T5488: LimitBoneWeightsProcess begin
	Debug, T5488: LimitBoneWeightsProcess end
	Debug, T5488: END   `postprocess`, dt= 0.001 s
	
	
	Debug, T5488: START `postprocess`
	Debug, T5488: ImproveCacheLocalityProcess begin
	Debug, T5488: Mesh 0 | ACMR in: 0.851622 out: 0.718139 | ~15.7
	Info,  T5488: Cache relevant are 1 meshes (251904 faces). Average output ACMR is 0.718139
	Debug, T5488: ImproveCacheLocalityProcess finished.
	Debug, T5488: END   `postprocess`, dt= 1.903 s
	
	
	Info,  T5488: Leaving post processing pipeline
	Debug, T5488: END   `total`, dt= 11.269 s

In this particular example only one fourth of the total import time was spent on the actual importing, while the rest of the
time got consumed by the #aiProcess_Triangulate, #aiProcess_JoinIdenticalVertices and #aiProcess_ImproveCacheLocality
postprocessing steps. A wise selection of postprocessing steps is therefore essential to getting good performance.
Of course this depends on the individual requirements of your application, in many of the typical use cases of assimp performance won't
matter (i.e. in an offline content pipeline).

.. _ai_threading:

Threading
---------
You can use the Asset-Importer-Library in a separate thread context. Just make sure that the resources used by the thread are not shared. 
At this moment, assimp will not make sure that it is safe over different thread contexts.

.. _ai_overview:

Overview
--------

This page discusses both **Assimp** scalability in threaded environments and the precautions to be taken in order to
use it from multiple threads concurrently.

.. _ai_threadsafety:

Thread-safety / using Assimp concurrently from several threads
--------------------------------------------------------------

The library can be accessed by multiple threads simultaneously, as long as the
following prerequisites are fulfilled:

 * Users of the C++-API should ensure that they use a dedicated #Assimp::Importer instance for each thread. 
   Constructing instances of #Assimp::Importer is expensive, so it might be a good idea to
   let every thread maintain its own thread-local instance (which can be used to
   load as many files as necessary).
 * The C-API is thread-safe.
 * When supplying custom IO logic, one must make sure the underlying implementation is thread-safe.
 * Custom log streams or logger replacements have to be thread-safe, too.

Multiple concurrent imports may or may not be beneficial, however. For certain file formats in conjunction with
little or no post-processing IO times tend to be the performance bottleneck. Intense post-processing together
with 'slow' file formats like X or Collada might scale well with multiple concurrent imports.


.. _ai_automt:

Internal threading
------------------

Internal multi-threading is not currently implemented.

.. _ai_res:

Resources
---------

This page lists some useful resources for **Assimp**. Note that, even though the core team has an eye on them,
we cannot guarantee the accuracy of third-party information. If in doubt, it's best to ask either on the
mailing list or on our forums on SF.net.

 * **Assimp** comes with some sample applications, these can be found in the <i>./samples</i> folder. Don't forget to read the <i>README</i> file.
 * `Assimp-GL-Demo <http://www.drivenbynostalgia.com/files/AssimpOpenGLDemo.rar>`_ - OpenGl animation sample using the library's animation import facilities.
 * `Assimp-Animation-Loader <http://nolimitsdesigns.com/game-design/open-asset-import-library-animation-loader/>`_ is another utility to
   simplify animation playback.
 * `Assimp-Animations <http://ogldev.atspace.co.uk/www/tutorial22/tutorial22.html>`_ - Tutorial "Loading models using the Open Asset Import Library", out of a series of OpenGL tutorials.

.. _ai_importer_notes:

Importer Notes
==============

.. _ai_blender:

Blender
-------

This section contains implementation notes for the Blender3D importer.

**Important:  the Blender importer is deprecated.**

.. _ai_bl_overview:

Overview
--------

**Assimp** provides a self-contained reimplementation of Blender's so-called SDNA system ( `Notes on SDNA http://www.blender.org/development/architecture/notes-on-sdna/`_ ).
SDNA allows Blender to be fully backward and forward-compatible and to exchange
files across all platforms. The BLEND format is thus a non-trivial binary monster and the loader tries to read the most of it,
naturally limited by the scope of the #aiScene output data structure.
Consequently, if Blender is the only modeling tool in your asset workflow, consider writing a
custom exporter from Blender if **Assimp** format coverage does not meet the requirements.

.. _ai_bl_status:

Current status
--------------

The Blender loader does not support animations yet, but is apart from that considered relatively stable.

@subsection bl_notes Notes

When filing bugs on the Blender loader, always give the Blender version (or, even better, post the file that caused the error).

.. _ai_ifc_overview:

IFC
---

This section contains implementation notes on the IFC-STEP importer.


.. _ai_ifc_overview:

Overview
--------

The library provides a partial implementation of the IFC2x3 industry standard for automatized exchange of CAE/architectural
data sets. See `IFC <http://en.wikipedia.org/wiki/Industry_Foundation_Classes>`_ for more information on the format. We aim
at getting as much 3D data out of the files as possible.

.. _ai_ifc_status:

Current status
--------------

IFC support is new and considered experimental. Please report any bugs you may encounter.

.. _ai_ifc_notes:

Notes
-----

- Only the STEP-based encoding is supported. IFCZIP and IFCXML are not (but IFCZIP can simply be unzipped to get a STEP file).
- The importer leaves vertex coordinates untouched, but applies a global scaling to the root transform to
  convert from whichever unit the IFC file uses to <i>metres</i>.
- If multiple geometric representations are provided, the choice of which one to load is based on how expensive a representation seems
  to be in terms of import time. The loader also avoids representation types for which it has known deficits.
- Not supported are arbitrary binary operations (binary clipping is implemented, though).
- Of the various relationship types that IFC knows, only aggregation, containment and material assignment are resolved and mapped to
  the output graph.
- The implementation knows only about IFC2X3 and applies this rule set to all models it encounters,
  regardless of their actual version. Loading of older or newer files may fail with parsing errors.

.. _ai_ifc_metadata:

Metadata
--------

IFC file properties (IfcPropertySet) are kept as per-node metadata, see aiNode::mMetaData.

.. _ai_ogre:

Ogre
----

**ATTENTION**: The Ogre-Loader is currently under development, many things have changed after this documentation was written, but they are not final enough to rewrite the documentation. So things may have changed by now!

This section contains implementations notes for the OgreXML importer.

.. _ai_ogre_overview:

Overview
--------

Ogre importer is currently optimized for the Blender Ogre exporter because that's the only one that I use. You can find the Blender Ogre exporter at: `OGRE3D forum <http://www.ogre3d.org/forums/viewtopic.php?f=8&t=45922>`_

.. _ai_what:

What will be loaded?
--------------------

Mesh: Faces, Positions, Normals, and all TexCoords. The Materialname will be used to load the material.

Material: The right material in the file will be searched, the importer should work with materials who
have 1 technique and 1 pass in this technique. From there, the texture name (for 1 color- and 1 normal map) and the
materialcolors (but not in custom materials) will be loaded. Also, the materialname will be set.

Skeleton: Skeleton with Bone hierarchy (Position and Rotation, but no Scaling in the skeleton is supported), names and transformations,
animations with rotation, translation and scaling keys.

.. _ai_export_Blender:

How to export Files from Blender
--------------------------------

You can find information about how to use the Ogreexporter on your own, so here are just some options that you need, so the assimp
importer will load everything correctly:

- Use either "Rendering Material" or "Custom Material" see @ref material
- do not use "Flip Up Axies to Y"
- use "Skeleton name follow mesh"


.. _ai_xml:

XML-Format
----------

There is a binary and an XML mesh Format from Ogre. This loader can only
Handle XML files, but don't panic, there is a command line converter, which you can use
to create XML files from Binary Files. Just look on the Ogre page for it.

Currently, you can only load meshes. So you will need to import the .mesh.xml file, the loader will
try to find the appendant material and skeleton file.

The skeleton file must have the same name as the mesh file, e.g. fish.mesh.xml and fish.skeleton.xml.

@subsection material Materials
The material file can have the same name as the mesh file (if the file is model.mesh or model.mesh.xml the
loader will try to load model.material),
or you can use 

::

	Importer::Importer::SetPropertyString(AI_CONFIG_IMPORT_OGRE_MATERIAL_FILE, "materiafile.material")
    
to specify the name of the material file. This is especially useful if multiple materials a stored in a single file.
The importer will first try to load the material with the same name as the mesh and only if this can't be opened try
to load the alternate material file. The default material filename is "Scene.material".

We suggest that you use custom materials, because they support multiple textures (like colormap and normalmap). First of all you
should read the custom material sektion in the Ogre Blender exporter Help File, and than use the assimp.tlp template, which you
can find in scripts/OgreImpoter/Assimp.tlp in the assimp source. If you don't set all values, don't worry, they will be ignored during import.

If you want more properties in custom materials, you can easily expand the ogre material loader, it will be just a few lines for each property.
Just look in OgreImporterMaterial.cpp

.. ai_importer:

Properties
----------

-	IMPORT_OGRE_TEXTURETYPE_FROM_FILENAME: Normally, a texture is loaded as a colormap, if no
	target is specified in the
	materialfile. Is this switch is enabled, texture names ending with _n, _l, _s
	are used as normalmaps, lightmaps or specularmaps.


	Property type: Bool. Default value: false.
-	IMPORT_OGRE_MATERIAL_FILE: Ogre Meshes contain only the MaterialName, not the MaterialFile.
	If there
	is no material file with the same name as the material, Ogre Importer will
	try to load this file and search the material in it.

	Property type: String. Default value: guessed.


.. _ai_properties:

Properties
----------

You can use properties to chance the behavior of you importer. In order to do so, you have to override BaseImporter::SetupProperties, and specify
you custom properties in config.h. Just have a look to the other AI_CONFIG_IMPORT_* defines and you will understand, how it works.

The properties can be set with Importer::SetProperty***() and can be accessed in your SetupProperties function with Importer::GetProperty***(). You can
store the properties as a member variable of your importer, they are thread safe.

.. _ai_tnote:

Notes for text importers
------------------------

* Try to make your parser as flexible as possible. Don't rely on particular layout, whitespace/tab style,
  except if the file format has a strict definition, in which case you should always warn about spec violations.
  But the general rule of thumb is *be strict in what you write and tolerant in what you accept*.
* Call **Assimp::BaseImporter::ConvertToUTF8()** before you parse anything to convert foreign encodings to UTF-8.
  That's not necessary for XML importers, which must use the provided XML-Parser for reading. 


.. _ai_bnote:

Notes for binary importers
--------------------------

* Take care of endianness issues! Assimp importers mostly support big-endian platforms, which define the <tt>AI_BUILD_BIG_ENDIAN</tt> constant.
  See the next section for a list of utilities to simplify this task.
* Don't trust the input data! Check all offsets!


.. _ai_util:

Utilities
---------

Mixed stuff for internal use by loaders, mostly documented (most of them are already included by *AssimpPCH.h*):

* **ByteSwapper** (*ByteSwapper.h*)   - manual byte swapping stuff for binary loaders.
* **StreamReader** (*StreamReader.h*) - safe, endianess-correct, binary reading.
* **XmlParser** (*XmlParser.hh*)      - The XML-Parser used in Asset-importer-Lib
* **CommentRemover** (*RemoveComments.h*) - remove single-line and multi-line comments from a text file.
* fast_atof, strtoul10, strtoul16, SkipSpaceAndLineEnd, SkipToNextToken .. large family of low-level
  parsing functions, mostly declared in *fast_atof.h*, *StringComparison.h* and *ParsingUtils.h* (a collection that grew
  historically, so don't expect perfect organization).
* **ComputeNormalsWithSmoothingsGroups()** (*SmoothingGroups.h*) - Computes normal vectors from plain old smoothing groups.
* **SkeletonMeshBuilder** (*SkeletonMeshBuilder.h*) - generate a dummy mesh from a given (animation) skeleton.
* **StandardShapes** (*StandardShapes.h*) - generate meshes for standard solids, such as platonic primitives, cylinders or spheres.
* **BatchLoader** (*BaseImporter.h*) - manage imports from external files. Useful for file formats
  which spread their data across multiple files.
* **SceneCombiner** (*SceneCombiner.h*) - exhaustive toolset to merge multiple scenes. Useful for file formats
  which spread their data across multiple files. 

.. _ai_mat:

Filling materials
-----------------

The required definitions zo set/remove/query keys in #ai_material structures are declared in *MaterialSystem.h*, in a
#aiMaterial derivate called #aiMaterial. The header is included by AssimpPCH.h, so you don't need to bother.

::

    aiMaterial* mat = new aiMaterial();

    const float spec = 16.f;
    mat->AddProperty(&spec, 1, AI_MATKEY_SHININESS);

    //set the name of the material:
    NewMaterial->AddProperty(&aiString(MaterialName.c_str()), AI_MATKEY_NAME);//MaterialName is a std::string

    //set the first diffuse texture
    NewMaterial->AddProperty(&aiString(Texturename.c_str()), AI_MATKEY_TEXTURE(aiTextureType_DIFFUSE, 0));//again, Texturename is a std::string

    
.. _ai_appa:

Appendix A 
===========
Template for BaseImporter's abstract methods
--------------------------------------------

::

    // -------------------------------------------------------------------------------
    // Returns whether the class can handle the format of the given file.
    bool xxxxImporter::CanRead( const std::string& pFile, IOSystem* pIOHandler,
          bool checkSig) const {
        const std::string extension = GetExtension(pFile);
        if(extension == "xxxx") {
            return true;
        }
        if (!extension.length() || checkSig) {
            // no extension given, or we're called a second time because no
            // suitable loader was found yet. This means, we're trying to open
            // the file and look for and hints to identify the file format.
            // #Assimp::BaseImporter provides some utilities:
            //
            // #Assimp::BaseImporter::SearchFileHeaderForToken - for text files.
            // It reads the first lines of the file and does a substring check
            // against a given list of 'magic' strings.
            //
            // #Assimp::BaseImporter::CheckMagicToken - for binary files. It goes
            // to a particular offset in the file and and compares the next words
            // against a given list of 'magic' tokens.

            // These checks MUST be done (even if !checkSig) if the file extension
            // is not exclusive to your format. For example, .xml is very common
            // and (co)used by many formats.
        }
        return false;
    }

    // -------------------------------------------------------------------------------
    // Get list of file extensions handled by this loader
    void xxxxImporter::GetExtensionList(std::set<std::string>& extensions) {
        extensions.insert("xxx");
    }

    // -------------------------------------------------------------------------------
    void xxxxImporter::InternReadFile( const std::string& pFile,
          aiScene* pScene, IOSystem* pIOHandler) {
        std::unique_ptr<IOStream> file( pIOHandler->Open( pFile, "rb"));

        // Check whether we can read from the file
        if( file.get() == NULL) {
            throw DeadlyImportError( "Failed to open xxxx file ", pFile, ".");
        }

        // Your task: fill pScene
        // Throw a ImportErrorException with a meaningful (!) error message if
        // something goes wrong.
    }
