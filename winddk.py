"""engine.SCons.Tool.msvc

Tool-specific initialization for Microsoft Visual C/C++.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "src/engine/SCons/Tool/msvc.py 2523 2007/12/12 09:37:41 knight"

import os.path
import re
import string

import SCons.Action
import SCons.Builder
import SCons.Errors
import SCons.Platform.win32
import SCons.Tool
import SCons.Tool.mslib
import SCons.Tool.mslink
import SCons.Util
import SCons.Warnings

CSuffixes = ['.c', '.C']
CXXSuffixes = ['.cc', '.cpp', '.cxx', '.c++', '.C++']

def get_winddk_paths(env, version=None):
    """Return a 3-tuple of (INCLUDE, LIB, PATH) as the values
    of those three environment variables that should be set
    in order to execute the MSVC tools properly."""
    
    WINDDKdir = None
    exe_paths = []
    lib_paths = []
    include_paths = []

    if 'BASEDIR' in os.environ:
        WINDDKdir = os.environ['BASEDIR']
    else:
        #WINDDKdir = "C:\\WINDDK\\3790.1830"
        WINDDKdir = "C:/WINDDK/3790.1830"

    exe_paths.append( os.path.join(WINDDKdir, 'bin') )
    exe_paths.append( os.path.join(WINDDKdir, 'bin/x86') )
    include_paths.append( os.path.join(WINDDKdir, 'inc/wxp') )
    lib_paths.append( os.path.join(WINDDKdir, 'lib') )

    target_os = 'wxp'
    target_cpu = 'i386'
    
    env['SDK_INC_PATH'] = os.path.join(WINDDKdir, 'inc', target_os) 
    env['CRT_INC_PATH'] = os.path.join(WINDDKdir, 'inc/crt') 
    env['DDK_INC_PATH'] = os.path.join(WINDDKdir, 'inc/ddk', target_os) 
    env['WDM_INC_PATH'] = os.path.join(WINDDKdir, 'inc/ddk/wdm', target_os) 

    env['SDK_LIB_PATH'] = os.path.join(WINDDKdir, 'lib', target_os, target_cpu) 
    env['CRT_LIB_PATH'] = os.path.join(WINDDKdir, 'lib/crt', target_cpu) 
    env['DDK_LIB_PATH'] = os.path.join(WINDDKdir, 'lib', target_os, target_cpu)
    env['WDM_LIB_PATH'] = os.path.join(WINDDKdir, 'lib', target_os, target_cpu)
                                     
    include_path = string.join( include_paths, os.pathsep )
    lib_path = string.join(lib_paths, os.pathsep )
    exe_path = string.join(exe_paths, os.pathsep )
    return (include_path, lib_path, exe_path)

def validate_vars(env):
    """Validate the PCH and PCHSTOP construction variables."""
    if env.has_key('PCH') and env['PCH']:
        if not env.has_key('PCHSTOP'):
            raise SCons.Errors.UserError, "The PCHSTOP construction must be defined if PCH is defined."
        if not SCons.Util.is_String(env['PCHSTOP']):
            raise SCons.Errors.UserError, "The PCHSTOP construction variable must be a string: %r"%env['PCHSTOP']

def pch_emitter(target, source, env):
    """Adds the object file target."""

    validate_vars(env)

    pch = None
    obj = None

    for t in target:
        if SCons.Util.splitext(str(t))[1] == '.pch':
            pch = t
        if SCons.Util.splitext(str(t))[1] == '.obj':
            obj = t

    if not obj:
        obj = SCons.Util.splitext(str(pch))[0]+'.obj'

    target = [pch, obj] # pch must be first, and obj second for the PCHCOM to work

    return (target, source)

def object_emitter(target, source, env, parent_emitter):
    """Sets up the PCH dependencies for an object file."""

    validate_vars(env)

    parent_emitter(target, source, env)

    if env.has_key('PCH') and env['PCH']:
        env.Depends(target, env['PCH'])

    return (target, source)

def static_object_emitter(target, source, env):
    return object_emitter(target, source, env,
                          SCons.Defaults.StaticObjectEmitter)

def shared_object_emitter(target, source, env):
    return object_emitter(target, source, env,
                          SCons.Defaults.SharedObjectEmitter)

pch_action = SCons.Action.Action('$PCHCOM', '$PCHCOMSTR')
pch_builder = SCons.Builder.Builder(action=pch_action, suffix='.pch',
                                    emitter=pch_emitter,
                                    source_scanner=SCons.Tool.SourceFileScanner)
res_action = SCons.Action.Action('$RCCOM', '$RCCOMSTR')
res_builder = SCons.Builder.Builder(action=res_action,
                                    src_suffix='.rc',
                                    suffix='.res',
                                    src_builder=[],
                                    source_scanner=SCons.Tool.SourceFileScanner)
SCons.Tool.SourceFileScanner.add_scanner('.rc', SCons.Defaults.CScan)

def generate(env):
    """Add Builders and construction variables for MSVC++ to an Environment."""
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)

    for suffix in CSuffixes:
        static_obj.add_action(suffix, SCons.Defaults.CAction)
        shared_obj.add_action(suffix, SCons.Defaults.ShCAction)
        static_obj.add_emitter(suffix, static_object_emitter)
        shared_obj.add_emitter(suffix, shared_object_emitter)

    for suffix in CXXSuffixes:
        static_obj.add_action(suffix, SCons.Defaults.CXXAction)
        shared_obj.add_action(suffix, SCons.Defaults.ShCXXAction)
        static_obj.add_emitter(suffix, static_object_emitter)
        shared_obj.add_emitter(suffix, shared_object_emitter)

    env['CCPDBFLAGS'] = SCons.Util.CLVar(['${(PDB and "/Z7") or ""}'])
    env['CCPCHFLAGS'] = SCons.Util.CLVar(['${(PCH and "/Yu%s /Fp%s"%(PCHSTOP or "",File(PCH))) or ""}'])
    env['CCCOMFLAGS'] = '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS /c $SOURCES /Fo$TARGET $CCPCHFLAGS $CCPDBFLAGS'
    env['CC']         = 'cl'
    env['CCFLAGS']    = SCons.Util.CLVar('/nologo')
    env['CFLAGS']     = SCons.Util.CLVar('')
    env['CCCOM']      = '$CC $CFLAGS $CCFLAGS $CCCOMFLAGS'
    env['SHCC']       = '$CC'
    env['SHCCFLAGS']  = SCons.Util.CLVar('$CCFLAGS')
    env['SHCFLAGS']   = SCons.Util.CLVar('$CFLAGS')
    env['SHCCCOM']    = '$SHCC $SHCFLAGS $SHCCFLAGS $CCCOMFLAGS'
    env['CXX']        = '$CC'
    env['CXXFLAGS']   = SCons.Util.CLVar('$CCFLAGS $( /TP $)')
    env['CXXCOM']     = '$CXX $CXXFLAGS $CCCOMFLAGS'
    env['SHCXX']      = '$CXX'
    env['SHCXXFLAGS'] = SCons.Util.CLVar('$CXXFLAGS')
    env['SHCXXCOM']   = '$SHCXX $SHCXXFLAGS $CCCOMFLAGS'
    env['CPPDEFPREFIX']  = '/D'
    env['CPPDEFSUFFIX']  = ''
    env['INCPREFIX']  = '/I'
    env['INCSUFFIX']  = ''
#    env.Append(OBJEMITTER = [static_object_emitter])
#    env.Append(SHOBJEMITTER = [shared_object_emitter])
    env['STATIC_AND_SHARED_OBJECTS_ARE_THE_SAME'] = 1

    env['RC'] = 'rc'
    env['RCFLAGS'] = SCons.Util.CLVar('')
    env['RCCOM'] = '$RC $_CPPDEFFLAGS $_CPPINCFLAGS $RCFLAGS /fo$TARGET $SOURCES'
    env['BUILDERS']['RES'] = res_builder
    env['OBJPREFIX']      = ''
    env['OBJSUFFIX']      = '.obj'
    env['SHOBJPREFIX']    = '$OBJPREFIX'
    env['SHOBJSUFFIX']    = '$OBJSUFFIX'

    try:
        include_path, lib_path, exe_path = get_winddk_paths(env)

        # since other tools can set these, we just make sure that the
        # relevant stuff from MSVS is in there somewhere.
        env.PrependENVPath('INCLUDE', include_path)
        env.PrependENVPath('LIB', lib_path)
        env.PrependENVPath('PATH', exe_path)
    except (SCons.Util.RegError, SCons.Errors.InternalError):
        pass

    env['CFILESUFFIX'] = '.c'
    env['CXXFILESUFFIX'] = '.cc'

    env['PCHPDBFLAGS'] = SCons.Util.CLVar(['${(PDB and "/Yd") or ""}'])
    env['PCHCOM'] = '$CXX $CXXFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS /c $SOURCES /Fo${TARGETS[1]} /Yc$PCHSTOP /Fp${TARGETS[0]} $CCPDBFLAGS $PCHPDBFLAGS'
    env['BUILDERS']['PCH'] = pch_builder

    env['AR']          = 'lib'
    env['ARFLAGS']     = SCons.Util.CLVar('/nologo')
    env['ARCOM']       = "${TEMPFILE('$AR $ARFLAGS /OUT:$TARGET $SOURCES')}"
    env['LIBPREFIX']   = ''
    env['LIBSUFFIX']   = '.lib'

    SCons.Tool.mslink.generate(env)

    # See also:
    # - WINDDK's bin/makefile.new i386mk.inc for more info.
    # - http://alter.org.ua/docs/nt_kernel/vc8_proj/
    env.Append(CPPDEFINES = [
        'WIN32', 
        '_WINDOWS', 
        ('i386', '1'), 
        ('_X86_', '1'), 
        'STD_CALL', 
        ('CONDITION_HANDLING', '1'),
        ('NT_INST', '0'), 
        ('_NT1X_', '100'),
        ('WINNT', '1'),
        ('_WIN32_WINNT', '0x0500'), # minimum required OS version
        ('WIN32_LEAN_AND_MEAN', '1'),
        ('DEVL', '1'),
        ('FPO', '1'),
    ])
    cflags = [
        '/GF', # Enable String Pooling
        '/GX-', # Disable C++ Exceptions
        '/Zp8', # 8bytes struct member alignment
        #'/GS-', # No Buffer Security Check
        '/GR-', # Disable Run-Time Type Info
        '/Gz', # __stdcall Calling convention
    ]
    env.Append(CFLAGS = cflags)
    env.Append(CXXFLAGS = cflags)
    
    env.Append(LINKFLAGS = [
        '/DEBUG',
        '/NODEFAULTLIB',
        '/SUBSYSTEM:NATIVE',
        '/INCREMENTAL:NO',
        #'/DRIVER', 
    
        #'-subsystem:native,4.00',
        '-base:0x10000',
        
        '-entry:DrvEnableDriver',
    ])
    
    if not env.has_key('ENV'):
        env['ENV'] = {}
    if not env['ENV'].has_key('SystemRoot'):    # required for dlls in the winsxs folders
        env['ENV']['SystemRoot'] = SCons.Platform.win32.get_system_root()

def exists(env):
    return env.Detect('cl')

