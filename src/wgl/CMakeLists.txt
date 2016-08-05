include_directories (
	${OPENGL_INCLUDE_PATH}
	${GLAD_INCLUDE_DIR}
	${CMAKE_SOURCE_DIR}/src/xdemos
)

link_libraries (
	${OPENGL_gl_LIBRARY}
	glad
)

add_executable (wglthreads wglthreads.c)
add_executable (wgl_sharedtex_mt sharedtex_mt.c)
set_target_properties (wgl_sharedtex_mt PROPERTIES OUTPUT_NAME sharedtex_mt)

add_executable (wglinfo wglinfo.c ${CMAKE_SOURCE_DIR}/src/xdemos/glinfo_common.c)
add_executable (wglcontext wglcontext.c)
add_executable (wincopy WIN32 wincopy.c wglutil.c)
add_executable (wglfontbitmaps wglfontbitmaps.c)
add_executable (wglfontoutlines wglfontoutlines.c)
add_executable (wglgears wglgears.c)

install (
	TARGETS
		wglthreads
		wgl_sharedtex_mt
		wglinfo
		wglcontext
		wglfontbitmaps
		wglfontoutlines
		wglgears
		wincopy
	DESTINATION wgl)
