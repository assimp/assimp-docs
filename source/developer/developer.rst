.. image:: https://www.assimp.org/common/images/splash-color.png

.. _developer_guide:
.. _ai_extend:

===================
The Developer Guide
===================

.. _ai_general:

Write your own importer
-----------------------

In this chapter, you will learn how to write your own importers. You just need to implement the #Assimp::BaseImporter class,
which defines a few abstract methods, registers your loader, tests it carefully and provides test models for it.

* Create a header-file **FormatNameImporter.h** and a cpp-unit ( **FormatNameImporter.cpp** ) in the **<root>/code/AssetLib/** directory
* Add them to the following workspaces: CMAKE (code/CMakeLists.txt, create a new source group for your importer and put them also to ADD_LIBRARY( assimp SHARED))
* Include *AssimpPCH.h* - this is the PCH file, and it already includes most Assimp-internal stuff.
* Open ImporterRegistry.cpp.cpp and include your header just below the *(include_new_importers_here)* line, guarded by a #define

::

    #if (!defined assimp_BUILD_NO_FormatName_IMPORTER)
        ...
    #endif

Wrap the same guard around your .cpp!

* Now advance to the **(register_new_importers_here)** line in the **ImporterRegistry.cpp** and register your importer there - just like all the others do.
* Set up a suitable test environment (i.e. use AssimpView or your own application), make sure to enable
  the #aiProcess_ValidateDataStructure flag, and enable verbose logging. That is, call before you import anything:

:: 

    DefaultLogger::create("AssimpLog.txt",Logger::VERBOSE)
    
* Implement the **Assimp::BaseImporter::CanRead()** : here the format detection will be perfoormed. You can detect the format by its extension or by parsing some token of the file content
* Implement **Assimp::BaseImporter::InternReadFile()**: Here you have to parse the file format and convert it into an aiScene-Instance:
* Implement **Assimp::BaseImporter::GetExtensionList()**: here you have to add the provided extensions (for the Wavefront-Files add .obj for instance).
* For error handling, throw a dynamic allocated **ImportErrorException** (see Appendix A) for critical errors, and log errors, warnings, info, and debug info
  with **DefaultLogger::get()->[error, warn, debug, info]**.
* A simple example:

::

    class MyyImporter : public BaseImporter {
    public:
        MyyImporter() : BaseImporter = default;
        
        MyyImporter() override = default;
        
        bool CanRead(const std::string &filename, IOSystem *pIOHandler, bool checkSig) const override {
            if (checkSig) {
                // Check the signature and return the result
            } else {
                const std::string extension = GetExtension(filename));
                if ( extension == "myExt) {
                    return true;
                }
            }
            return false;
        }
            
        void InternReadFile() {
            // Add your code here
        }
    };

::

* Make sure that your loader compiles against all build configurations on all supported platforms. You can use our CI-build to check several platforms 
  like Windows and Linux (32-bit and 64-bit).
* Provide some _free_ test models in <root>/test/models/<FormatName> and credit their authors.
  Test files for a file format shouldn't be too large (*~500 KiB in total*), and not too repetitive. Try to cover all format features with test data.
* Done! Please, share your loader so that everyone can profit from it!

Write your own exporter
-----------------------

ToDo!

Write your own unit / integration-test
--------------------------------------
After the importer and the exporter is ready you need to test them. The common way of doing this will be explained in this chapter. Assimp does provide 
some useful test utilities for importer and exporter testing. 

Start writing test code for your importer and exporter by creating a test class at **test/unit/ImportExport/<YourImporterName>**. 
Check the following example to get a better understanding of how your test class shall look like:

::

    #include "AbstractImportExportBase.h"
    #include "UnitTestPCH.h"
    // Add more depending includes based on your test

    class utMyImporter : public AbstractImportExportBase {
    public:
        bool importerTest() override {
            Assimp::Importer importer;
            const aiScene *scene = importer.ReadFile(ASSIMP_TEST_MODELS_DIR "/MyFormat/Wuson.myformat", aiProcess_ValidateDataStructure);
            return nullptr != scene;
        }
    };

    TEST_F(utMyImporter, importTest) {
        EXPECT_TRUE(importerTest());
    }


Add this to the **CMakeLists.txt** at **test/unit/CMakeLists.txt** and run the build. Add your basic test file at **test/models/MyFormat**.
Now you can run the test:
* Navigate into the binary folder
* Execute the application **unit** or **unit.exe** on Windows-Platforms.
* Check your result and fix it until all tests are green again.

These tests will run for each PR as a test. The CI will also check your code for leaks or undefined behaviors.


Parser tools
------------

XML-Parser:
###########
To use the XML-Parser you need to follow these steps:
- Include the header XmlParser.h
- Create an XML-Parser instance
- Load the data from an input stream into the parser
- Perform the parsing
- When this was successful, iterate over the XML-Nodes:

::

    #include <assimp/XmlParser.h>
    
    void parse_and_validate_xml(Stream *mySteam) {
      // Read the data and parse the XML-File
      XMLParser xmlParser;
      if (xmlParser.parse(stream)) {
         // Get the root node
         XmlNode node = xmlParser.getRootNode();
         
         // Find one special child node
         XmlNode colladaNode = node.child("COLLADA");
         
         // Iterate over all children
         for ( auto child : colladaNode.children()) {
         }
      }
    }

::

You can also iterate over all children nodes via an Iterator interface:

::

    XmlNodeIterator xmlIt(node, XmlNodeIterator::PreOrderMode);
    XmlNode currentNode;
    while (xmlIt.getNext(currentNode)) {
      // all nodes will be iterated level wise
    }

::
