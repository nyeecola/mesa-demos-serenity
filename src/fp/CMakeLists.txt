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

set (subdir fp)

set (targets
	fp-tri
	tri-depth
	tri-depth2
	tri-depthwrite
	tri-depthwrite2
	tri-param
	tri-tex
	point-position
)

foreach (target ${targets})
	add_executable (${subdir}_${target} ${target}.c)
	set_target_properties (${subdir}_${target} PROPERTIES OUTPUT_NAME ${target})
	install (TARGETS ${subdir}_${target} DESTINATION ${subdir})
endforeach (target)

file (GLOB data *.txt)

install (FILES ${data} DESTINATION ${subdir})
