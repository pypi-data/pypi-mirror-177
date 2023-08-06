#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fastwfc::fastwfc" for configuration "Release"
set_property(TARGET fastwfc::fastwfc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fastwfc::fastwfc PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libfastwfc.a"
  )

list(APPEND _cmake_import_check_targets fastwfc::fastwfc )
list(APPEND _cmake_import_check_files_for_fastwfc::fastwfc "${_IMPORT_PREFIX}/lib/libfastwfc.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
