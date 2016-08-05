AM_CFLAGS = \
	$(DEMO_CFLAGS) \
	$(GLUT_CFLAGS) \
	-I$(top_srcdir)/src/glad/include \
	-I$(top_srcdir)/src/util
AM_LDFLAGS = \
	$(DEMO_LIBS) \
	$(GLUT_LIBS)

if HAVE_GLUT
bin_PROGRAMS = \
	gs-tri
endif

LDADD = ../glad/libglad.la

EXTRA_DIST = \
	basic.glsl
