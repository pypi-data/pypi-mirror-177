#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "VTK::Addon" for configuration "Release"
set_property(TARGET VTK::Addon APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(VTK::Addon PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "VTK::CommonMath"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/vtkmodules/libvtkAddon.so.0.1.0"
  IMPORTED_SONAME_RELEASE "libvtkAddon.so.1"
  )

list(APPEND _cmake_import_check_targets VTK::Addon )
list(APPEND _cmake_import_check_files_for_VTK::Addon "${_IMPORT_PREFIX}/lib/vtkmodules/libvtkAddon.so.0.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
