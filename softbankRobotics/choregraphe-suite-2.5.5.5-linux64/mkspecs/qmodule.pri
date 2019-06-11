CONFIG +=  compile_examples qpa largefile precompile_header sse2 sse3 ssse3 sse4_1 sse4_2 avx pcre
QT_BUILD_PARTS +=  tools libs
QT_NO_DEFINES =  ALSA CUPS GLIB IMAGEFORMAT_JPEG OPENVG PULSEAUDIO STYLE_GTK
QT_QCONFIG_PATH = 
host_build {
    QT_CPU_FEATURES.x86_64 =  mmx sse sse2
} else {
    QT_CPU_FEATURES.x86_64 =  mmx sse sse2
}
QT_COORD_TYPE = double
QT_LFLAGS_ODBC   = -lodbc
styles += mac fusion windows
DEFINES += QT_NO_MTDEV
QMAKE_CFLAGS_FONTCONFIG = -I/usr/include/freetype2  
QMAKE_LIBS_FONTCONFIG = -lfontconfig -lfreetype  
DEFINES += QT_NO_LIBUDEV
QMAKE_X11_PREFIX = /usr
QMAKE_XKB_CONFIG_ROOT = /usr/share/X11/xkb
QMAKE_INCDIR_EGL = /usr/include/libdrm  
QMAKE_LIBS_EGL = -lEGL  
QMAKE_CFLAGS_EGL =  
QMAKE_CFLAGS_XCB =  
QMAKE_LIBS_XCB = -lxcb  
sql-drivers = 
sql-plugins =  sqlite
