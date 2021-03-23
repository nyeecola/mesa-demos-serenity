#!/bin/bash

if [ -d /usr/lib/ccache ]
then
	export PATH="/usr/lib/ccache:$PATH"
fi

set -e -x -u

GLUT_INCLUDE_DIR="$PWD/external/freeglut/include"
GLUT_LIBRARY="$PWD/external/freeglut/lib/libfreeglut.a"
if [ ! -f "$GLUT_INCLUDE_DIR/GL/glut.h" ]
then
	mkdir -p "$GLUT_INCLUDE_DIR/GL"
	for header in GL/glut.h GL/freeglut.h GL/freeglut_std.h GL/freeglut_ext.h
	do
		cp -av "/usr/include/$header" "$GLUT_INCLUDE_DIR/$header"
	done
fi
if [ ! -f "$GLUT_LIBRARY" ]
then
	mkdir -p external/freeglut/lib
	i686-w64-mingw32-dlltool --kill-at --def .gitlab-ci/freeglut.def --output-lib "$GLUT_LIBRARY"
fi

cmake \
	-S . \
	-B build/mingw32 \
	-G "Ninja" \
	-DCMAKE_TOOLCHAIN_FILE=.gitlab-ci/mingw32.cmake \
	-DCMAKE_BUILD_TYPE=Debug \
	-DCMAKE_INSTALL_PREFIX=publish/mingw32 \
	-DGLUT_INCLUDE_DIR="$GLUT_INCLUDE_DIR" \
	-DGLUT_glut_LIBRARY="$GLUT_LIBRARY" \
	-DGLUT_glut_LIBRARY_DEBUG="$GLUT_LIBRARY" \
	-DGLUT_glut_LIBRARY_RELEASE="$GLUT_LIBRARY"

cmake --build build/mingw32

cmake --build build/mingw32 --target install
