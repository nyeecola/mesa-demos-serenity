include_directories (include)

set (GLAD_SOURCES src/glad.c)
if (WIN32)
	set (GLAD_SOURCES ${GLAD_SOURCES} src/glad_wgl.c)
endif ()

add_library (glad STATIC
	${GLAD_SOURCES}
)
