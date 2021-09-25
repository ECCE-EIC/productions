#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "eicsmear::eicsmear" for configuration ""
set_property(TARGET eicsmear::eicsmear APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(eicsmear::eicsmear PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libeicsmear.so"
  IMPORTED_SONAME_NOCONFIG "libeicsmear.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS eicsmear::eicsmear )
list(APPEND _IMPORT_CHECK_FILES_FOR_eicsmear::eicsmear "${_IMPORT_PREFIX}/lib/libeicsmear.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
