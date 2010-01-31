#line 205 "interscript/src/iscr.pak"
# interscript package
import string
def hexval(i):
  i = i.upper()
  if i[:2]=='0X': i = i[2:]
  a = 0
  for d in i:
    a = a * 16 + ord(d) - {0:ord('0'), 1:ord('A')-10}[d>'9']
  return a

__builtins__['hexval']=hexval

import os
directory = os.path.split(__file__)[0]+os.sep
def bind_resource_name(*components):
  return directory + os.path.join(*components)

#line 254 "interscript/src/iscr.pak"
import interscript.drivers
import interscript.drivers.sinks
import interscript.drivers.sources
import interscript.drivers.storage
import interscript.weavers
import interscript.tanglers
import interscript.core

class global_frame:

  from interscript.drivers.sinks.bufdisk import named_file_sink
  from interscript.drivers.sinks.disk import simple_named_file_sink
  from interscript.drivers.sinks.null import null_sink
  from interscript.drivers.sinks.cache import cache_sink

  from interscript.drivers.sources.base import eoi, eof
  from interscript.drivers.sources.disk import named_file_source
  from interscript.drivers.sources.url import url_source
  from interscript.drivers.sources.cache import cache_source

  from interscript.drivers.storage.memory import memory

  from interscript.weavers.auto import auto_weaver
  from interscript.weavers.filter import markup_filter
  from interscript.weavers.multiplexor import multiplexor

  from interscript.parsers.html import sgml_wrapper, html_filter

  from interscript.tanglers.data import data_tangler
  from interscript.tanglers.python import python_tangler
  from interscript.tanglers.null import null_tangler
  from interscript.tanglers.doc import doc_tangler
  import sys
  import os
  import string
  import re
  import time
  from interscript.utilities import commands
  from interscript.core.sets import set
  from interscript.core.stacks import stack
  import interscript.core.protocols
  protocol = interscript.core.protocols
  from . import getoptions

  import builtins
  __builtins__ = builtins
  del builtins

  try:
    import _thread
    #print 'thread available'
  except:
    #print 'thread NOT available'
    pass

#line 349 "interscript/src/iscr.pak"
# first a hack to help bootstrapping work
# if any of the variable in the second section don't exist.
# then the at least some value is set in the generated code.
# Iterated bootstrapping should eventually fix the problem.

  buildno=0
  version=0
  hostname="unknown"
  username="unknown"
  buildtime="unknown"
  generator_buildno=0
  generator_hostname="unknown"
  generator_username="unknown"
  generator_version="unknown"
  generator_buildtime="unknown"

# now the real data
  buildno=117
  version='1.0a11'
  hostname='pelican'
  username='skaller'
  buildtime='Wed Jun 04, 2003 at 05:32 AM (UTC)'
  generator_buildno=116
  generator_hostname='pelican'
  generator_username='skaller'
  generator_version='1.0a11'
  generator_buildtime='Wed Jun 04, 2003 at 05:24 AM (UTC)'

# now define a routine to print the current version information
# wrapped in try/except clause in case any of the variables didn't get set
def print_version_info():
  try:
    print('Interscript version',global_frame.version, end=' ')
    print('build',global_frame.buildno)
    print('Built by',global_frame.username, end=' ')
    print('on',global_frame.hostname, end=' ')
    print('at',global_frame.buildtime)
    print('Generated by',global_frame.generator_version, end=' ')
    print('buildno',global_frame.generator_buildno, end=' ')
    print('host',global_frame.generator_hostname)
    print('at',global_frame.buildtime)
  except: pass
#line 394 "interscript/src/iscr.pak"
# This is a utility function that makes it easy to use interscript
# givem options in a standard form. The arguments are a list as
# would be entered on a unix or nt command line.
# Mac (or Tkinter) users can create a GUI interface to set the options
# and then call this function to run interscript.

def run_from_options(arguments):
  from interscript.getframes import getoption_frames
  from interscript.frames.processf import process_frame
  process_options, master_options = getoption_frames(arguments)
  process = process_frame(global_frame, process_options, master_options)
  process.run()
  del process

