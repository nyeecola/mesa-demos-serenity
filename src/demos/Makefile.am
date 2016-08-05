# Copyright © 2009 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# Authors:
#    Eric Anholt <eric@anholt.net>

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
	arbfplight \
	arbfslight \
	arbocclude \
	arbocclude2 \
	bounce \
	clearspd \
	copypix \
	cubemap \
	cuberender \
	dinoshade \
	dissolve \
	drawpix \
	engine \
	fbo_firecube \
	fbotexture \
	fire \
	fogcoord \
	fplight \
	fslight \
	gamma \
	gearbox \
	gears \
	geartrain \
	glinfo \
	gloss \
	gltestperf \
	ipers \
	isosurf \
	lodbias \
	morph3d \
	multiarb \
	paltex \
	pixeltest \
	pointblast \
	projtex \
	ray \
	readpix \
	reflect \
	renormal \
	shadowtex \
	singlebuffer \
	spectex \
	spriteblast \
	stex3d \
	teapot \
	terrain \
	tessdemo \
	texcyl \
	texenv \
	textures \
	trispd \
	tunnel2 \
	tunnel \
	vao_demo \
	winpos
endif

tunnel_SOURCES = \
	tunnel.c \
	tunneldat.h

LDADD = ../glad/libglad.la
copypix_LDADD = ../util/libutil.la ../glad/libglad.la
cubemap_LDADD = ../util/libutil.la ../glad/libglad.la
cuberender_LDADD = ../util/libutil.la ../glad/libglad.la
drawpix_LDADD = ../util/libutil.la ../glad/libglad.la
dissolve_LDADD = ../util/libutil.la ../glad/libglad.la
engine_LDADD = ../util/libutil.la ../glad/libglad.la
fbo_firecube_LDADD = ../util/libutil.la ../glad/libglad.la
fire_LDADD = ../util/libutil.la ../glad/libglad.la
gloss_LDADD = ../util/libutil.la ../glad/libglad.la
ipers_LDADD = ../util/libutil.la ../glad/libglad.la
isosurf_LDADD = ../util/libutil.la ../glad/libglad.la
lodbias_LDADD = ../util/libutil.la ../glad/libglad.la
multiarb_LDADD = ../util/libutil.la ../glad/libglad.la
projtex_LDADD = ../util/libutil.la ../glad/libglad.la
readpix_LDADD = ../util/libutil.la ../glad/libglad.la
reflect_LDADD = ../util/libutil.la ../glad/libglad.la
teapot_LDADD = ../util/libutil.la ../glad/libglad.la
texcyl_LDADD = ../util/libutil.la ../glad/libglad.la
textures_LDADD = ../util/libutil.la ../glad/libglad.la
tunnel_LDADD = ../util/libutil.la ../glad/libglad.la
tunnel2_LDADD = ../util/libutil.la ../glad/libglad.la
winpos_LDADD = ../util/libutil.la ../glad/libglad.la

EXTRA_DIST = \
	README
