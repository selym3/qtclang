# qtclang

Small PyQt GUI for C/C++ applications

## Instructions

* Put `qtclang.py` inside of C or C++ directory
* Check the `main()` function for the configuration settings
  * Change compiler
  * Change object file extension
  * Change source directory
  * Change output directory
  * Change project/main file path
  * Width and height of the gui window
* It is not recommended to use absolute paths, meaning you should always run it locally.
  * This is because if there are duplicate folder names in the absolute path, it is possible that the wrong one will be replaced with the output directory when generating output paths for all the source files.

## TODO

* Add safe output file path generation from source path to allow for absolute paths (although this might not be necessary / possible).
* Add option to load up with flags and add config file option (that will be used if present)
