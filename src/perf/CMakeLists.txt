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

set (subdir perf)

set (targets
	copytex
	drawoverhead
	fbobind
	fill
	genmipmap
	glslstateschange
	readpixels
	swapbuffers
	teximage
	vbo
	vertexrate
)

foreach (target ${targets})
	add_executable (${subdir}_${target} ${target}.c common.c glmain.c)
	set_target_properties (${subdir}_${target} PROPERTIES OUTPUT_NAME ${target})
	install (TARGETS ${subdir}_${target} DESTINATION ${subdir})
endforeach (target)

add_executable (glsl-compile-time glsl-compile-time.c)
install (TARGETS glsl-compile-time DESTINATION ${subdir})
