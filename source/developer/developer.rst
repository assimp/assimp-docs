.. _developer_guide:

The Developer Guide
===================

.. _ai_extend:

Extending the Library
---------------------

.. _ai_general:

General
-------

Or - how to write your own loaders. It's easy. You just need to implement the #Assimp::BaseImporter class,
which defines a few abstract methods, register your loader, test it carefully and provide test models for it.

OK, that sounds too easy :-). The whole procedure for a new loader merely looks like this:

* Create a header (*FormatNameImporter.h*) and a unit (*FormatNameImporter.cpp*) in the *<root>/code/AssetLib/* directory
* Add them to the following workspaces: vc8 and vc9 (the files are in the workspaces directory), CMAKE (code/CMakeLists.txt, create a new source group for your importer and put them also to ADD_LIBRARY( assimp SHARED))
* Include *AssimpPCH.h* - this is the PCH file, and it includes already most Assimp-internal stuff.
* Open ImporterRegistry.cpp.cpp and include your header just below the *(include_new_importers_here)* line, guarded by a #define

::

    #if (!defined assimp_BUILD_NO_FormatName_IMPORTER)
        ...
    #endif

Wrap the same guard around your .cpp!

* Now advance to the *(register_new_importers_here)* line in the ImporterRegistry.cpp and register your importer there - just like all the others do.
* Setup a suitable test environment (i.e. use AssimpView or your own application), make sure to enable
  the #aiProcess_ValidateDataStructure flag and enable verbose logging. That is, simply call before you import anything:

:: 

    DefaultLogger::create("AssimpLog.txt",Logger::VERBOSE)
    
* Implement the Assimp::BaseImporter::CanRead(), Assimp::BaseImporter::InternReadFile() and Assimp::BaseImporter::GetExtensionList().
  Just copy'n'paste the template from Appendix A and adapt it for your needs.
* For error handling, throw a dynamic allocated ImportErrorException (see Appendix A) for critical errors, and log errors, warnings, infos and debuginfos
  with DefaultLogger::get()->[error, warn, debug, info].
* Make sure that your loader compiles against all build configurations on all supported platforms. You can use our CI-build to check several platforms 
  like Windows and Linux ( 32 bit and 64 bit ).
* Provide some _free_ test models in <root>/test/models/<FormatName> and credit their authors.
  Test files for a file format shouldn't be too large (*~500 KiB in total*), and not too repetive. Try to cover all format features with test data.
* Done! Please, share your loader that everyone can profit from it!
