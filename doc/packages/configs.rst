Package: src/packages/configs.fdoc


================
Platform configs
================


====================== =====================================
key                    file                                  
====================== =====================================
flx_config.py          $PWD/buildsystem/flx_config.py        
flx_config_ncurses.flx $PWD/src/tools/flx_config_ncurses.flx 
====================== =====================================

======================================== ============================================================
key                                      file                                                         
======================================== ============================================================
linux64_gcc_flx_rtl_config_params.hpp    $PWD/src/config/linux64/gcc/rtl/flx_rtl_config_params.hpp    
macosx64_clang_flx_rtl_config_params.hpp $PWD/src/config/macosx64/clang/rtl/flx_rtl_config_params.hpp 
macosx64_gcc_flx_rtl_config_params.hpp   $PWD/src/config/macosx64/gcc/rtl/flx_rtl_config_params.hpp   
win64_msvc_flx_rtl_config_params.hpp     $PWD/src/config/win64/msvc/rtl/flx_rtl_config_params.hpp     
======================================== ============================================================

================================= =====================================================
key                               file                                                  
================================= =====================================================
linux64_demux_sockety_config.hpp  $PWD/src/config/linux64/rtl/demux_sockety_config.hpp  
macosx64_demux_sockety_config.hpp $PWD/src/config/macosx64/rtl/demux_sockety_config.hpp 
win64_demux_sockety_config.hpp    $PWD/src/config/win64/rtl/demux_sockety_config.hpp    
================================= =====================================================

=========== ===============================
key         file                            
=========== ===============================
linux.flxh  $PWD/src/config/linux/flx.flxh  
macosx.flxh $PWD/src/config/macosx/flx.flxh 
win.flxh    $PWD/src/config/win/flx.flxh    
=========== ===============================

================ ==============================
key              file                           
================ ==============================
cplusplus_11.hpp share/lib/rtl/cplusplus_11.hpp 
cplusplus_14.hpp share/lib/rtl/cplusplus_14.hpp 
cplusplus_17.hpp share/lib/rtl/cplusplus_17.hpp 
cplusplus_20.hpp share/lib/rtl/cplusplus_20.hpp 
================ ==============================

====================== ======================================
key                    file                                   
====================== ======================================
clang_cplusplus_11.fpc $PWD/src/config/clang/cplusplus_11.fpc 
clang_cplusplus_14.fpc $PWD/src/config/clang/cplusplus_14.fpc 
clang_cplusplus_17.fpc $PWD/src/config/clang/cplusplus_17.fpc 
clang_cplusplus_20.fpc $PWD/src/config/clang/cplusplus_20.fpc 
====================== ======================================

==================== ====================================
key                  file                                 
==================== ====================================
gcc_cplusplus_11.fpc $PWD/src/config/gcc/cplusplus_11.fpc 
gcc_cplusplus_14.fpc $PWD/src/config/gcc/cplusplus_14.fpc 
gcc_cplusplus_17.fpc $PWD/src/config/gcc/cplusplus_17.fpc 
gcc_cplusplus_20.fpc $PWD/src/config/gcc/cplusplus_20.fpc 
==================== ====================================


===================== =====================================
key                   file                                  
===================== =====================================
msvc_cplusplus_11.fpc $PWD/src/config/msvc/cplusplus_11.fpc 
msvc_cplusplus_14.fpc $PWD/src/config/msvc/cplusplus_14.fpc 
msvc_cplusplus_17.fpc $PWD/src/config/msvc/cplusplus_17.fpc 
msvc_cplusplus_20.fpc $PWD/src/config/msvc/cplusplus_20.fpc 
===================== =====================================


test stuff
==========




.. image:: hello.jpg



OSX
===


.. code-block:: cpp

  //[macosx64_demux_sockety_config.hpp ]
  #ifndef __DEMUX_SOCKETY_CONFIG_H__
  #define __DEMUX_SOCKETY_CONFIG_H__
  #include <sys/socket.h>
  typedef socklen_t FLX_SOCKLEN_T;
  #endif


.. code-block:: cpp

  //[macosx64_clang_flx_rtl_config_params.hpp ]
  #ifndef __FLX_RTL_CONFIG_PARAMS_H__
  #define __FLX_RTL_CONFIG_PARAMS_H__
  
  #define FLX_HAVE_VSNPRINTF 1
  #define FLX_HAVE_GNU 1
  #define FLX_HAVE_GNU_BUILTIN_EXPECT 1
  #define FLX_HAVE_CGOTO 0
  #define FLX_HAVE_ASM_LABELS 0
  #define FLX_HAVE_DLOPEN 1
  #define FLX_CYGWIN 0
  #define FLX_MACOSX 1
  #define FLX_LINUX 0
  #define FLX_WIN32 0
  #define FLX_WIN64 0
  #define FLX_POSIX 1
  #define FLX_SOLARIS 0
  #define FLX_HAVE_MSVC 0
  #define FLX_HAVE_KQUEUE_DEMUXER 1
  #define FLX_HAVE_POLL 1
  #define FLX_HAVE_EPOLL 0
  #define FLX_HAVE_EVTPORTS 0
  #define FLX_HAVE_OPENMP 0
  #define FLX_MAX_ALIGN 16
  #endif


.. code-block:: cpp

  //[macosx64_gcc_flx_rtl_config_params.hpp ]
  #ifndef __FLX_RTL_CONFIG_PARAMS_H__
  #define __FLX_RTL_CONFIG_PARAMS_H__
  
  #define FLX_HAVE_VSNPRINTF 1
  #define FLX_HAVE_GNU 1
  #define FLX_HAVE_GNU_BUILTIN_EXPECT 1
  #define FLX_HAVE_CGOTO 1
  #define FLX_HAVE_ASM_LABELS 1
  #define FLX_HAVE_DLOPEN 1
  #define FLX_CYGWIN 0
  #define FLX_MACOSX 1
  #define FLX_LINUX 0
  #define FLX_WIN32 0
  #define FLX_WIN64 0
  #define FLX_POSIX 1
  #define FLX_SOLARIS 0
  #define FLX_HAVE_MSVC 0
  #define FLX_HAVE_KQUEUE_DEMUXER 1
  #define FLX_HAVE_POLL 1
  #define FLX_HAVE_EPOLL 0
  #define FLX_HAVE_EVTPORTS 0
  #define FLX_HAVE_OPENMP 0
  #define FLX_MAX_ALIGN 16
  #endif


Linux
=====


.. code-block:: cpp

  //[linux64_demux_sockety_config.hpp ]
  #ifndef __DEMUX_SOCKETY_CONFIG_H__
  #define __DEMUX_SOCKETY_CONFIG_H__
  #include <sys/socket.h>
  typedef socklen_t FLX_SOCKLEN_T;
  #endif


.. code-block:: cpp

  //[linux64_gcc_flx_rtl_config_params.hpp ]
  #ifndef __FLX_RTL_CONFIG_PARAMS_H__
  #define __FLX_RTL_CONFIG_PARAMS_H__
  
  #define FLX_HAVE_VSNPRINTF 1
  #define FLX_HAVE_GNU 1
  #define FLX_HAVE_GNU_BUILTIN_EXPECT 1
  #define FLX_HAVE_CGOTO 1
  #define FLX_HAVE_ASM_LABELS 1
  #define FLX_HAVE_DLOPEN 1
  #define FLX_CYGWIN 0
  #define FLX_MACOSX 0
  #define FLX_LINUX 1
  #define FLX_WIN32 0
  #define FLX_WIN64 0
  #define FLX_POSIX 1
  #define FLX_SOLARIS 0
  #define FLX_HAVE_MSVC 0
  #define FLX_HAVE_KQUEUE_DEMUXER 0
  #define FLX_HAVE_POLL 1
  #define FLX_HAVE_EPOLL 1
  #define FLX_HAVE_EVTPORTS 0
  #define FLX_HAVE_OPENMP 1
  #define FLX_MAX_ALIGN 16
  #endif


Windows
=======


.. code-block:: cpp

  //[win64_msvc_flx_rtl_config_params.hpp ]
  #ifndef __FLX_RTL_CONFIG_PARAMS_H__
  #define __FLX_RTL_CONFIG_PARAMS_H__
  
  #define FLX_HAVE_VSNPRINTF 1
  #define FLX_HAVE_GNU 0
  #define FLX_HAVE_GNU_BUILTIN_EXPECT 0
  #define FLX_HAVE_CGOTO 0
  #define FLX_HAVE_ASM_LABELS 0
  #define FLX_HAVE_DLOPEN 0
  #define FLX_CYGWIN 0
  #define FLX_MACOSX 0
  #define FLX_LINUX 0
  #define FLX_WIN32 1
  #define FLX_WIN64 1
  #define FLX_POSIX 0
  #define FLX_SOLARIS 0
  #define FLX_HAVE_MSVC 1
  #define FLX_HAVE_KQUEUE_DEMUXER 0
  #define FLX_HAVE_POLL 0
  #define FLX_HAVE_EPOLL 0
  #define FLX_HAVE_EVTPORTS 0
  #define FLX_HAVE_OPENMP 1
  #define FLX_MAX_ALIGN 16
  #endif


.. code-block:: cpp

  //[win64_demux_sockety_config.hpp]
  #ifndef __DEMUX_SOCKETY_CONFIG_H__
  #define __DEMUX_SOCKETY_CONFIG_H__
  namespace flx { namespace demux {
  DEMUX_EXTERN  int create_listener_socket (int *io_port, int q_len);
  DEMUX_EXTERN  int create_async_listener(int *io_port, int q_len);
  DEMUX_EXTERN  int nice_accept(int *listener, int *err);
  DEMUX_EXTERN  int nice_connect(char const* addr, int port);
  DEMUX_EXTERN  int async_connect(char const* addr, int port, int *finished, int *err);
  DEMUX_EXTERN  int bind_sock(int s, int *io_port);
  DEMUX_EXTERN  int make_nonblock(int s);
  DEMUX_EXTERN  int make_linger(int s, int t);
  DEMUX_EXTERN  int set_tcp_nodelay(int s, int dsable_nagle);
  DEMUX_EXTERN  int get_socket_error(int s, int *socket_err);
  }}
  
  #endif
  

.. code-block:: text

  macro val PLAT_POSIX = true;
  macro val PLAT_LINUX = true;
  macro val PLAT_BSD = false;
  macro val PLAT_MACOSX = false;
  macro val PLAT_CYGWIN = false;
  macro val PLAT_WIN32 = false;
  macro val PLAT_SOLARIS = false;

.. code-block:: text

  macro val PLAT_POSIX = true;
  macro val PLAT_LINUX = false;
  macro val PLAT_BSD = true;
  macro val PLAT_MACOSX = true;
  macro val PLAT_CYGWIN = false;
  macro val PLAT_WIN32 = false;
  macro val PLAT_SOLARIS = false;

.. code-block:: text

  macro val PLAT_POSIX = false;
  macro val PLAT_LINUX = false;
  macro val PLAT_BSD = false;
  macro val PLAT_MACOSX = false;
  macro val PLAT_CYGWIN = false;
  macro val PLAT_WIN32 = true;
  macro val PLAT_SOLARIS = false;


C++ Standard Versions
=====================



.. code-block:: cpp

  //[cplusplus_11.hpp]
  #if __cplusplus < 201103L 
  #error "C++11 required"
  #endif

.. code-block:: cpp

  //[cplusplus_14.hpp]
  #if __cplusplus < 201402L
  #error "C++11 required"
  #endif

.. code-block:: cpp

  //[cplusplus_17.hpp]
  #if __cplusplus < 201703L 
  #error "C++11 required"
  #endif

.. code-block:: cpp

  //[cplusplus_20.hpp]
  #if __cplusplus < 202003L 
  #error "C++11 required"
  #endif


.. code-block:: fpc

  //[clang_cplusplus_11.fpc]
  Description: C++11 required
  includes: '"cplusplus_11.hpp"'
  cflags: -std=c++11

.. code-block:: fpc

  //[clang_cplusplus_14.fpc]
  Description: C++14 required
  includes: '"cplusplus_14.hpp"'
  cflags: -std=c++14

.. code-block:: fpc

  //[clang_cplusplus_17.fpc]
  Description: C++17 required
  includes: '"cplusplus_17.hpp"'
  cflags: -std=c++17

.. code-block:: fpc

  //[clang_cplusplus_20.fpc]
  Description: C++20 required
  includes: '"cplusplus_20.hpp"'
  cflags: -std=c++20


.. code-block:: fpc

  //[gcc_cplusplus_11.fpc]
  Description: C++11 required
  includes: '"cplusplus_11.hpp"'
  cflags: -std=c++11

.. code-block:: fpc

  //[gcc_cplusplus_14.fpc]
  Description: C++14 required
  includes: '"cplusplus_14.hpp"'
  cflags: -std=c++14

.. code-block:: fpc

  //[gcc_cplusplus_17.fpc]
  Description: C++17 required
  includes: '"cplusplus_17.hpp"'
  cflags: -std=c++17

.. code-block:: fpc

  //[gcc_cplusplus_20.fpc]
  Description: C++20 required
  includes: '"cplusplus_20.hpp"'
  cflags: -std=c++20

.. code-block:: fpc

  //[msvc_cplusplus_11.fpc]
  Description: C++11 required
  includes: '"cplusplus_11.hpp"'
  cflags: -std:c++11

.. code-block:: fpc

  //[msvc_cplusplus_14.fpc]
  Description: C++14 required
  includes: '"cplusplus_14.hpp"'
  cflags: -std:c++14

.. code-block:: fpc

  //[msvc_cplusplus_17.fpc]
  Description: C++17 required
  includes: '"cplusplus_17.hpp"'
  cflags: -std:c++17

.. code-block:: fpc

  //[msvc_cplusplus_20.fpc]
  Description: C++20 required
  includes: '"cplusplus_20.hpp"'
  cflags: -std:c++20


.. code-block:: python

  #[flx_config.py]
  from fbuild.path import Path
  import buildsystem
  from os import getenv
  
  def target_config(ctx,target,os,bits,compiler):
      print("[fbuild] COPYING UNIVERSAL RESOURCE DATABASE")
      buildsystem.copy_to(ctx, ctx.buildroot/'host/config', Path('src/config/*.fpc').glob())
  
      print("[fbuild] COPYING compiler/C++ version RESOURCE DATABASE")
      buildsystem.copy_to(ctx, ctx.buildroot / 'host/config', Path('src/config/'+compiler+'/*.fpc').glob())
  
      print("[fbuild] COPYING generic unix RESOURCE DATABASE")
      if 'posix' in target.platform: 
        buildsystem.copy_to(ctx, ctx.buildroot / 'host/config', Path('src/config/unix/*.fpc').glob())
        buildsystem.copy_to(ctx, ctx.buildroot / 'host/config', Path('src/config/unix'+bits+'/*.fpc').glob())
  
      print("[fbuild] COPYING " + os + " RESOURCE DATABASE")
      buildsystem.copy_to(ctx, ctx.buildroot / 'host/config', Path('src/config/'+os+'/*.fpc').glob())
  
      print("[fbuild] COPYING " + os + bits + " RESOURCE DATABASE")
      buildsystem.copy_to(ctx, ctx.buildroot / 'host/config', Path('src/config/'+os+bits+'/*.fpc').glob())
  
      print("[fbuild] COPYING " + os + " PLAT MACROS")
      buildsystem.copy_to(ctx, ctx.buildroot / 'host/lib/plat', Path('src/config/'+os+'/*.flxh').glob())
  
      print("C[fbuild] OPYING "+os+bits+"/"+compiler+" RTL CONFIG")
      buildsystem.copy_to(ctx, ctx.buildroot/'host/lib/rtl', Path('src/config/'+os+bits+'/'+compiler+'/rtl/*.hpp').glob())
  
      print("[fbuild] COPYING "+os+bits+" SOCKET CONFIG")
      buildsystem.copy_to(ctx, ctx.buildroot/'host/lib/rtl', Path('src/config/'+os+bits+'/rtl/*.hpp').glob())
  
      home = getenv("HOME")
      if home is not None:
          print("COPYING USER CONFIG DATA FROM " + home+"/.felix/config")
          buildsystem.copy_fpc_to_config(ctx, Path(home, ".felix", "config", "*.fpc").glob())
  
      # set the toolchain
      dst = ctx.buildroot / 'host/config/toolchain.fpc'
      if 'macosx' in target.platform:
          toolchain = "toolchain_"+compiler+"_macosx"
      elif "windows" in target.platform:
          toolchain= "toolchain_msvc_win"
      else:
          toolchain = "toolchain_"+compiler+"_linux"
  
      print("**********************************************")
      print("SETTING TOOLCHAIN " + toolchain)
      print("**********************************************")
      f = open(dst,"w")
      f.write ("toolchain: "+toolchain+"\n")
      f.close()


.. code-block:: felix

  //[flx_config_ncurses.flx]
  include "std/io/ncurses";
  open Ncurses;
  open C_hack;
  
  proc config() {
    var w = initscr();
  
    var install  = array_calloc[char] 40;
    var target   = array_calloc[char] 40;
    var compiler = array_calloc[char] 40;
    var wordsize = array_calloc[char] 40;
    var os       = array_calloc[char] 40;
  
    mvwprintw(0,0,w, c"Felix target configuration tool");
    mvwprintw(1,0,w, c"INSTALL DIRECTORY:          ");
    mvwprintw(2,0,w, c"Target Subdirectory Name:   ");
    mvwprintw(3,0,w, c"Compiler family:            ");
    mvwprintw(4,0,w, c"Word size:                  ");
    mvwprintw(5,0,w, c"OS name:                    ");
  
    mvwgetstr(1,30,install);
    mvwgetstr(2,30,target);
    mvwgetstr(3,30,compiler);
    mvwgetstr(4,30,wordsize);
    mvwgetstr(5,30,os);
  
    free install;
    free target;
    free compiler;
    free worsize;
    free os;
   
    ignore$ #refresh;
    ignore$ wgetch(w);
    ignore$ #endwin;
    
  }
  config;


