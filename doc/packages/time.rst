Package: src/packages/time.fdoc


===========
Time of Day
===========

============== ============================
key            file                         
============== ============================
time.flx       share/lib/std/time.flx       
posix_time.flx share/lib/std/posix/time.flx 
win32_time.flx share/lib/std/win32/time.flx 
============== ============================


RTC: Time of Day
================

A Real Time Clock (RTC) is a device that provides the
current date and time of day.


.. index:: Time_class(class)
.. index:: time(gen)
.. index:: Time(class)
.. code-block:: felix

  //[time.flx]
  class Time_class [os] {
    virtual gen time: 1 -> double; // time in seconds since Jan 1 1970 UTC, seconds
  }
  
  open class Time {
  if PLAT_WIN32 do
    inherit Win32Time;
  else
    inherit PosixTime;
  done
    rename fun sleep =  Faio::sleep; 
  
  }
  
  
Posix RTC
=========



.. index:: PosixTime(class)
.. index:: system_timepoint(type)
.. index:: system_duration(type)
.. index:: system_clock_now(gen)
.. index:: double(ctor)
.. code-block:: felix

  //[posix_time.flx]
  
  class PosixTime
  {
    requires Posix_headers::sys_time_h;
  
    private type time_t = "time_t";
    private type suseconds_t = "suseconds_t";
  
    private fun _ctor_double: time_t -> double = "static_cast<double>($1)";
    private fun _ctor_double: suseconds_t -> double = "static_cast<double>($1)";
  
    private cstruct timeval {
      tv_sec: time_t;
      tv_usec: suseconds_t;
    };
  
    private proc gettimeofday: &timeval = "gettimeofday($1, NULL);";
  
    inherit Time_class[Posix];
  
    instance Time_class[Posix] {
      gen time () : double = {
        var tv:timeval;
        gettimeofday(&tv);
        return tv.tv_sec.double + tv.tv_usec.double / 1.0e6;
      }
    }
  
    type system_timepoint  = "::std::chrono::time_point<::std::chrono::system_clock>"
      requires Cxx11_headers::chrono, Cxx11_headers::ratio
    ;
  
    type system_duration = "::std::chrono::system_clock::duration"
      requires Cxx11_headers::chrono, Cxx11_headers::ratio
    ;
  
    gen system_clock_now : 1 -> system_timepoint = "::std::chrono::system_clock::now()";
  
    // elapsed time
    fun -: system_timepoint * system_timepoint -> system_duration = "$1-$2";
    
    ctor double : system_duration = """
      ((::std::chrono::duration<double>($1)).count())
    """;
  
  }
  
Win32 RTC
=========


.. index:: Win32Time(class)
.. code-block:: felix

  //[win32_time.flx]
  
  class Win32Time
  {
    requires Posix_headers::sys_types_h;
    requires Win32_headers::sys_timeb_h;
  
    private type time_t = "time_t";
    private fun _ctor_double: time_t -> double = "static_cast<double>($1)";
  
    private cstruct __timeb64 {
      time: time_t; // seconds
      millitm: ushort; // milliseconds
    };
  
    private proc _ftime64_s: &__timeb64 = "_ftime64_s($1);";
  
    inherit Time_class[Win32];
  
    instance Time_class[Win32] {
      gen time () : double = {
        var tv:__timeb64;
        _ftime64_s(&tv);
        return tv.time.double + tv.millitm.double / 1.0e3;
      }
    }
  }
  
