.. image:: https://www.assimp.org/common/images/splash-color.png

.. _developer_guide:
.. _ai_extend:

===================
The Developer Guide
===================

.. _ai_general:

Write your own importer
-----------------------

In this chapter you will learn how to write your own importers. You just need to implement the #Assimp::BaseImporter class,
which defines a few abstract methods, register your loader, test it carefully and provide test models for it.

* Create a header-file **FormatNameImporter.h** and a cpp-unit ( **FormatNameImporter.cpp** ) in the **<root>/code/AssetLib/** directory
* Add them to the following workspaces: CMAKE (code/CMakeLists.txt, create a new source group for your importer and put them also to ADD_LIBRARY( assimp SHARED))
* Include *AssimpPCH.h* - this is the PCH file, and it includes already most Assimp-internal stuff.
* Open ImporterRegistry.cpp.cpp and include your header just below the *(include_new_importers_here)* line, guarded by a #define

::

    #if (!defined assimp_BUILD_NO_FormatName_IMPORTER)
        ...
    #endif

Wrap the same guard around your .cpp!

* Now advance to the **(register_new_importers_here)** line in the **ImporterRegistry.cpp** and register your importer there - just like all the others do.
* Setup a suitable test environment (i.e. use AssimpView or your own application), make sure to enable
  the #aiProcess_ValidateDataStructure flag and enable verbose logging. That is, simply call before you import anything:

:: 

    DefaultLogger::create("AssimpLog.txt",Logger::VERBOSE)
    
* Implement the **Assimp::BaseImporter::CanRead()** : here the format detection will be perfoormed. You can detect the format by its extension or by parsing some token of the file content
* Implement **Assimp::BaseImporter::InternReadFile()** : Here you have to parse the file fomat and convert it into a aiScene-Instance:
* Implement **Assimp::BaseImporter::GetExtensionList()** : here you have to add the provided extensions (for the Wavefront-Files add .obj for instance).
* For error handling, throw a dynamic allocated **ImportErrorException** (see Appendix A) for critical errors, and log errors, warnings, infos and debuginfos
  with **DefaultLogger::get()->[error, warn, debug, info]**.
* A simple example:

::

    class MyyImporter : public BaseImporter {
    public:
        MyyImporter() : BaseImporter {}
        
        MyyImporter() override {}
        
        bool CanRead(const std::string &filename, IOSystem *pIOHandler, bool checkSig) const override {
            if (checkSig) {
                // Check the signature and return result
            } else {
                const std::string extension = GetExtension(filename));
                if ( extension == "myExt) {
                    return true;
                }
            }
            return false;
        }
            
        void InternReadFile()       {}
        
    };

::

* Make sure that your loader compiles against all build configurations on all supported platforms. You can use our CI-build to check several platforms 
  like Windows and Linux ( 32 bit and 64 bit ).
* Provide some _free_ test models in <root>/test/models/<FormatName> and credit their authors.
  Test files for a file format shouldn't be too large (*~500 KiB in total*), and not too repetive. Try to cover all format features with test data.
* Done! Please, share your loader that everyone can profit from it!

Write your own exporter
-----------------------

ToDo!


Parser tools
------------

XML-Parser:
###########
To use the XML-Parser you need to follow these steps:
- Include the header XmlParser.h
- Create a XML-Parser instance
- Load the data from an input stream into the parser
- Perform the parsing
- When this was succesful, iterate over the XML-Nodes:

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
      // all node will be iterated level wise
    }

::
