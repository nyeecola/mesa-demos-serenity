/*
 * Copyright (C) 2011 Morgan Armand <morgan.devel@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
 * AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <glad/glad.h>
#include <glad/glad_wgl.h>

static LRESULT CALLBACK
WndProc(HWND hWnd,
        UINT uMsg,
        WPARAM wParam,
        LPARAM lParam )
{
   switch (uMsg) {
   case WM_DESTROY:
      PostQuitMessage(0);
      break;
   default:
      return DefWindowProc(hWnd, uMsg, wParam, lParam);
   }

   return 0;
}

static const char *
context_error_to_string(DWORD error)
{
   switch (error) {
   case ERROR_INVALID_VERSION_ARB:  return "ERROR_INVALID_VERSION_ARB";
   case ERROR_INVALID_PROFILE_ARB:  return "ERROR_INVALID_PROFILE_ARB";
   case ERROR_INVALID_OPERATION:    return "ERROR_INVALID_OPERATION";
   case ERROR_DC_NOT_FOUND:         return "ERROR_DC_NOT_FOUND";
   case ERROR_INVALID_PIXEL_FORMAT: return "ERROR_INVALID_PIXEL_FORMAT";
   case ERROR_NO_SYSTEM_RESOURCES:  return "ERROR_NO_SYSTEM_RESOURCES";
   case ERROR_INVALID_PARAMETER:    return "ERROR_INVALID_PARAMETER";
   default:                         return "Unknown Error";
   }
}

static char *
profile_mask_to_string(GLint profileMask)
{
   switch (profileMask) {
   case GL_CONTEXT_CORE_PROFILE_BIT:
      return "GL_CONTEXT_CORE_PROFILE_BIT";
   case GL_CONTEXT_COMPATIBILITY_PROFILE_BIT:
      return "GL_CONTEXT_COMPATIBILITY_PROFILE_BIT";
   default:
      return "0";
   }
}

static char *
context_flags_to_string(GLint flags)
{
   static char buf[1000] = {0};
   if (flags & GL_CONTEXT_FLAG_FORWARD_COMPATIBLE_BIT)
      strcat(buf, "GL_CONTEXT_FLAG_FORWARD_COMPATIBLE_BIT | ");
   if (flags & GL_CONTEXT_FLAG_DEBUG_BIT)
      strcat(buf, "GL_CONTEXT_FLAG_DEBUG_BIT | ");
   if (flags & GL_CONTEXT_FLAG_ROBUST_ACCESS_BIT)
      strcat(buf, "GL_CONTEXT_FLAG_ROBUST_ACCESS_BIT | ");
   if (flags & GL_CONTEXT_FLAG_NO_ERROR_BIT_KHR)
      strcat(buf, "GL_CONTEXT_FLAG_NO_ERROR_BIT_KHR | ");

   int n = strlen(buf);
   if (n >= 3) {
      /* rm the trailing " | " */
      buf[n-3] = 0;
   }
   else {
      strcat(buf, "(none)");
   }

   return buf;
}

static void
print_context_infos(void)
{
   GLint majorVersion;
   GLint minorVersion;
   GLint profileMask, flags;
   const char *version, *vendor, *renderer;

   fprintf(stdout, "Context Informations\n");

   version = (const char *)glGetString(GL_VERSION);
   fprintf(stdout, "GL_VERSION: %s\n", version);

   vendor = (const char *)glGetString(GL_VENDOR);
   fprintf(stdout, "GL_VENDOR: %s\n", vendor);

   renderer = (const char *)glGetString(GL_RENDERER);
   fprintf(stdout, "GL_RENDERER: %s\n", renderer);

   // Request informations with the new 3.x features.
   if (sscanf(version, "%d.%d", &majorVersion, &minorVersion) != 2)
      return;

   if (majorVersion >= 3) {
      glGetIntegerv(GL_MAJOR_VERSION, &majorVersion);
      glGetIntegerv(GL_MINOR_VERSION, &minorVersion);
      fprintf(stdout, "GL_MAJOR_VERSION: %d\n", majorVersion);
      fprintf(stdout, "GL_MINOR_VERSION: %d\n", minorVersion);
   }
   if (majorVersion * 10 + minorVersion >= 32) {
      glGetIntegerv(GL_CONTEXT_PROFILE_MASK, &profileMask);
      glGetIntegerv(GL_CONTEXT_FLAGS, &flags);
      fprintf(stdout, "GL_CONTEXT_PROFILE_MASK: %s\n",
              profile_mask_to_string(profileMask));
      fprintf(stdout, "GL_CONTEXT_FLAGS: %s\n",
              context_flags_to_string(flags));
   }

   /* Test if deprecated features work or generate an error */
   while (glGetError() != GL_NO_ERROR)
      ;

   (void) glGenLists(1);
   if (glGetError()) {
      fprintf(stdout, "glGenLists generated an error.\n");
   }
   else {
      fprintf(stdout, "glGenLists generated no error.\n");
   }
}

static void
create_context(int majorVersion, int minorVersion, int profileMask, int contextFlags)
{
   WNDCLASS wc;
   HWND win;
   HDC hdc;
   PIXELFORMATDESCRIPTOR pfd;
   int pixelFormat;
   HGLRC tmp, ctx;

   memset(&wc, 0, sizeof(wc));
   wc.style = CS_OWNDC | CS_HREDRAW | CS_VREDRAW;
   wc.lpfnWndProc = WndProc;
   wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
   wc.hCursor = LoadCursor(NULL, IDC_ARROW);
   wc.hbrBackground = (HBRUSH) (COLOR_BTNFACE + 1);
   wc.lpszClassName = "wglcontext";

   if (!RegisterClass(&wc)) {
      fprintf(stderr, "RegisterClass() failed\n");
      return;
   }

   win = CreateWindowEx(0,
                     wc.lpszClassName,
                     "wglinfo",
                     WS_CLIPSIBLINGS | WS_CLIPCHILDREN,
                     CW_USEDEFAULT,
                     CW_USEDEFAULT,
                     CW_USEDEFAULT,
                     CW_USEDEFAULT,
                     NULL,
                     NULL,
                     wc.hInstance,
                     NULL);
   if (!win) {
      fprintf(stderr, "CreateWindowEx() failed\n");
      return;
   }

   hdc = GetDC(win);
   if (!hdc) {
      fprintf(stderr, "GetDC() failed\n");
      return;
   }

   memset(&pfd, 0, sizeof(pfd));
   pfd.nSize = sizeof(pfd);
   pfd.nVersion = 1;
   pfd.dwFlags = PFD_DOUBLEBUFFER | PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL;
   pfd.iPixelType = PFD_TYPE_RGBA;
   pfd.cColorBits = 24;
   pfd.cDepthBits = 24;
   pfd.iLayerType = PFD_MAIN_PLANE;

   pixelFormat = ChoosePixelFormat(hdc, &pfd);
   if (!pixelFormat) {
      fprintf(stderr, "ChoosePixelFormat() failed\n");
      return;
   }

   if (!SetPixelFormat(hdc, pixelFormat, &pfd)) {
      fprintf(stderr, "SetPixelFormat() failed\n");
      return;
   }

   tmp = wglCreateContext(hdc);
   if (!tmp) {
      fprintf(stderr, "wglCreateContext() failed\n");
      return;
   }

   if (!wglMakeCurrent(hdc, tmp)) {
      fprintf(stderr, "wglMakeCurrent() failed\n");
      return;
   }

   gladLoadGL();
   gladLoadWGL(hdc);

   if (!GLAD_WGL_ARB_create_context) {
      fprintf(stderr, "wglCreateContextAttribsARB isn't supported\n");
      return;
   }

   int attribsList[20];
   int i = 0;
   attribsList[i++] = WGL_CONTEXT_MAJOR_VERSION_ARB;
   attribsList[i++] = majorVersion;
   attribsList[i++] = WGL_CONTEXT_MINOR_VERSION_ARB;
   attribsList[i++] = minorVersion;
   if (contextFlags) {
      attribsList[i++] = WGL_CONTEXT_FLAGS_ARB;
      attribsList[i++] = contextFlags;
   }
   if (profileMask) {
      attribsList[i++] = WGL_CONTEXT_PROFILE_MASK_ARB;
      attribsList[i++] = profileMask;
   }
   attribsList[i++] = 0;

   ctx = wglCreateContextAttribsARB(hdc, 0, attribsList);
   if (!ctx) {
      DWORD error = GetLastError();
      fprintf(stderr, "wglCreateContextAttribsARB failed(): %s (0x%lx)\n",
              context_error_to_string(error), error);
      return;
   }

   wglMakeCurrent(NULL, NULL);
   wglDeleteContext(tmp);

   if (!wglMakeCurrent(hdc, ctx)) {
      fprintf(stderr, "wglMakeCurrent() failed\n");
      return;
   }

   print_context_infos();
}

static void
usage(void)
{
   fprintf(stdout, "Usage: wglcontext [-h] [-major <major>] [-minor <minor>] [-core] [-compat] [-debug] [-forward]\n");
   fprintf(stdout, "   -major   : specify the major version you want\n");
   fprintf(stdout, "   -minor   : specify the minor version you want\n");
   fprintf(stdout, "   -core    : request a context implementing the core profile\n");
   fprintf(stdout, "   -compat  : request a context implementing the compatibility profile\n");
   fprintf(stdout, "   -debug   : request a debug context\n");
   fprintf(stdout, "   -forward : request a forward-compatible context\n");
}

int
main(int argc, char *argv[])
{
   int i;
   int majorVersion = 1, minorVersion = 0;
   int contextFlags = 0x0;
   int profileMask = 0x0;

   for (i = 1; i < argc; i++) {
      if (strcmp(argv[i], "-h") == 0) {
         usage();
         exit(0);
      }
      else if (strcmp(argv[i], "-major") == 0 && i + 1 < argc) {
         majorVersion = (int)strtol(argv[i + 1], (char **)NULL, 10);
         i++;
      }
      else if (strcmp(argv[i], "-minor") == 0 && i + 1 < argc) {
         minorVersion = (int)strtol(argv[i + 1], (char **)NULL, 10);
         i++;
      }
      else if (strcmp(argv[i], "-core") == 0) {
         profileMask = WGL_CONTEXT_CORE_PROFILE_BIT_ARB;
      }
      else if (strcmp(argv[i], "-compat") == 0) {
         profileMask = WGL_CONTEXT_COMPATIBILITY_PROFILE_BIT_ARB;
      }
      else if (strcmp(argv[i], "-debug") == 0) {
         contextFlags |= WGL_CONTEXT_DEBUG_BIT_ARB;
      }
      else if (strcmp(argv[i], "-forward") == 0) {
         contextFlags |= WGL_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB;
      }
      else {
         usage();
         exit(1);
      }
   }

   create_context(majorVersion, minorVersion,
                  profileMask, contextFlags);

   return 0;
}
