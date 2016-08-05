include_directories (
	${CMAKE_SOURCE_DIR}/src/util
	${OPENGL_INCLUDE_PATH}
	${GLUT_INCLUDE_DIR}
	${GLAD_INCLUDE_DIR}
)

link_directories (
	${CMAKE_SOURCE_DIR}/src/util
)

link_libraries (
	util
	${OPENGL_gl_LIBRARY}
	${OPENGL_glu_LIBRARY}
	${GLUT_glut_LIBRARY}
	glad
)


add_executable (objview
	glm.c
	glmdraw.c
	objview.c
	skybox.c
)
install (TARGETS objview DESTINATION objviewer)

file (GLOB data *.mtl *.obj *.rgb)

install (FILES ${data} DESTINATION objviewer)
