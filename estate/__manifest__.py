{
    # Module Name
    # Required
    name:"Testing module",
    # Module Summary
    # Optional
    summary: "",
    author:"",
    website:"",
    liscence:"",
    version:"1.0.0.0"
    # Modules that must be loaded before adding this.
    depends: ["base"]
    # List of paths of data files that must be installed/updated with module
    # Files are loaded in order of data array.
    data: [],
    # List of paths of data files that are used in demo mode
    demo:[],
    # True: will automatically installed if all dependecies are also installed
    auto_install: False,
    # A dictionary containing py/binary dependencies
    external_dependencies:dict()
}