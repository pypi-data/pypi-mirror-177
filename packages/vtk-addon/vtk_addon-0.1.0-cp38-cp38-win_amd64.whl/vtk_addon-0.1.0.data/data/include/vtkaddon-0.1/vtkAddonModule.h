
#ifndef VTK_ADDON_EXPORT_H
#define VTK_ADDON_EXPORT_H

#ifdef VTK_ADDON_STATIC_DEFINE
#  define VTK_ADDON_EXPORT
#  define VTK_ADDON_NO_EXPORT
#else
#  ifndef VTK_ADDON_EXPORT
#    ifdef Addon_EXPORTS
        /* We are building this library */
#      define VTK_ADDON_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define VTK_ADDON_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef VTK_ADDON_NO_EXPORT
#    define VTK_ADDON_NO_EXPORT 
#  endif
#endif

#ifndef VTK_ADDON_DEPRECATED
#  define VTK_ADDON_DEPRECATED __declspec(deprecated)
#endif

#ifndef VTK_ADDON_DEPRECATED_EXPORT
#  define VTK_ADDON_DEPRECATED_EXPORT VTK_ADDON_EXPORT VTK_ADDON_DEPRECATED
#endif

#ifndef VTK_ADDON_DEPRECATED_NO_EXPORT
#  define VTK_ADDON_DEPRECATED_NO_EXPORT VTK_ADDON_NO_EXPORT VTK_ADDON_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef VTK_ADDON_NO_DEPRECATED
#    define VTK_ADDON_NO_DEPRECATED
#  endif
#endif

#endif /* VTK_ADDON_EXPORT_H */
