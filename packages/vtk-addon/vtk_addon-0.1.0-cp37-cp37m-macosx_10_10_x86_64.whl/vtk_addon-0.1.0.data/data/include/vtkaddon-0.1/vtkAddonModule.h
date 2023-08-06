
#ifndef VTK_ADDON_EXPORT_H
#define VTK_ADDON_EXPORT_H

#ifdef VTK_ADDON_STATIC_DEFINE
#  define VTK_ADDON_EXPORT
#  define VTK_ADDON_NO_EXPORT
#else
#  ifndef VTK_ADDON_EXPORT
#    ifdef Addon_EXPORTS
        /* We are building this library */
#      define VTK_ADDON_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define VTK_ADDON_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef VTK_ADDON_NO_EXPORT
#    define VTK_ADDON_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef VTK_ADDON_DEPRECATED
#  define VTK_ADDON_DEPRECATED __attribute__ ((__deprecated__))
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
