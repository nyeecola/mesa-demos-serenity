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
AM_CXXFLAGS = \
	$(DEMO_CXXFLAGS) \
	$(GLUT_CXXFLAGS) \
	-I$(top_srcdir)/src/glad/include \
	-I$(top_srcdir)/src/util
AM_LDFLAGS = \
	$(DEMO_LIBS) \
	$(GLUT_LIBS)

if HAVE_GLUT
bin_PROGRAMS = \
	array \
        bezier \
	bitmap \
	brick \
	bump \
	blinking-teapot \
	convolutions \
	deriv \
	fragcoord \
	fsraytrace \
	geom-outlining-130 \
	geom-outlining-150 \
	geom-sprites \
	geom-stipple-lines \
	geom-wide-lines \
	gsraytrace \
	identity \
	linktest \
	mandelbrot \
	multinoise \
	multitex \
	noise2 \
	noise \
	pointcoord \
	points \
	samplers \
	samplers_array \
	shadow_sampler \
	shtest \
	simplex-noise \
	skinning \
	texaaline \
	texdemo1 \
	toyball \
	trirast \
	twoside \
	vert-or-frag-only \
	vert-tex \
	vsraytrace
endif

gsraytrace_SOURCES = gsraytrace.cpp

samplers_array_SOURCES = samplers.c
samplers_array_CFLAGS = $(AM_CFLAGS) -DSAMPLERS_ARRAY

LDADD = ../glad/libglad.la
array_LDADD = ../util/libutil.la ../glad/libglad.la
bitmap_LDADD = ../util/libutil.la ../glad/libglad.la
bezier_LDADD = ../util/libutil.la ../glad/libglad.la
brick_LDADD = ../util/libutil.la ../glad/libglad.la
bump_LDADD = ../util/libutil.la ../glad/libglad.la
blinking_teapot_LDADD = ../util/libutil.la ../glad/libglad.la
convolutions_LDADD = ../util/libutil.la ../glad/libglad.la
deriv_LDADD = ../util/libutil.la ../glad/libglad.la
geom_outlining_130_LDADD = ../util/libutil.la ../glad/libglad.la
geom_outlining_150_LDADD = ../util/libutil.la ../glad/libglad.la
geom_sprites_LDADD = ../util/libutil.la ../glad/libglad.la
geom_stipple_lines_LDADD = ../util/libutil.la ../glad/libglad.la
geom_wide_lines_LDADD = ../util/libutil.la ../glad/libglad.la
gsraytrace_LDADD = ../util/libutil.la ../glad/libglad.la
fsraytrace_LDADD = ../util/libutil.la ../glad/libglad.la
fragcoord_LDADD = ../util/libutil.la ../glad/libglad.la
identity_LDADD = ../util/libutil.la ../glad/libglad.la
linktest_LDADD = ../util/libutil.la ../glad/libglad.la
mandelbrot_LDADD = ../util/libutil.la ../glad/libglad.la
multitex_LDADD = ../util/libutil.la ../glad/libglad.la
noise_LDADD = ../util/libutil.la ../glad/libglad.la
simplex_noise_LDADD = ../util/libutil.la ../glad/libglad.la
pointcoord_LDADD = ../util/libutil.la ../glad/libglad.la
points_LDADD = ../util/libutil.la ../glad/libglad.la
samplers_LDADD = ../util/libutil.la ../glad/libglad.la
samplers_array_LDADD = ../util/libutil.la ../glad/libglad.la
shtest_LDADD = ../util/libutil.la ../glad/libglad.la
skinning_LDADD = ../util/libutil.la ../glad/libglad.la
texdemo1_LDADD = ../util/libutil.la ../glad/libglad.la
toyball_LDADD = ../util/libutil.la ../glad/libglad.la
trirast_LDADD = ../util/libutil.la ../glad/libglad.la
twoside_LDADD = ../util/libutil.la ../glad/libglad.la
vert_or_frag_only_LDADD = ../util/libutil.la ../glad/libglad.la
vert_tex_LDADD = ../util/libutil.la ../glad/libglad.la
vsraytrace_LDADD = ../util/libutil.la ../glad/libglad.la

EXTRA_DIST = \
	CH06-brick.frag \
	CH06-brick.vert \
	CH11-bumpmap.frag \
	CH11-bumpmap.vert \
	CH11-toyball.frag \
	CH11-toyball.vert \
	CH18-mandel.frag \
	CH18-mandel.vert \
        bezier.geom \
	brick.shtest \
	convolution.vert \
	cubemap.frag \
	mandelbrot.shtest \
	multitex.frag \
	multitex.shtest \
	multitex.vert \
	reflect.vert \
	shadowtex.frag \
	simple.vert \
	skinning.frag \
	toyball.shtest
