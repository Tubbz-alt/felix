Package: src/packages/reals.fdoc


=================
Approximate Reals
=================

================ =====================================
key              file                                  
================ =====================================
real.flx         share/lib/std/scalar/real.flx         
float_format.flx share/lib/std/scalar/float_format.flx 
================ =====================================


.. index:: zero(fun)
.. index:: neg(fun)
.. index:: one(fun)
.. index:: abs(fun)
.. index:: log10(fun)
.. index:: sqrt(fun)
.. index:: ceil(fun)
.. index:: floor(fun)
.. index:: trunc(fun)
.. index:: embed(fun)
.. index:: atan2(fun)
.. code-block:: felix

  //[real.flx]
  instance[t in numbers] FloatAddgrp[t] {
    fun zero: unit -> t = "(?1)0" ;
    fun + : t * t -> t = "$1+$2" ;
    fun neg : t -> t = "-$1" ;
    fun - : t * t -> t = "$1-$2" ;
    proc += : &t * t = "*$1+=$2;";
    proc -= : &t * t = "*$1-=$2;";
  }
  
  instance[t in numbers] FloatMultSemi1[t] {
    fun one: unit -> t = "(?1)1";
    fun * : t * t -> t = "$1*$2";
    proc *= : &t * t = "*$1*=$2;";
  }
  
  instance[t in numbers] FloatRing[t] {}
  instance[t in ints \cup complexes] FloatDring[t] {
    fun / : t * t -> t = "$1/$2";
    fun % : t * t -> t = "$1%$2";
    proc /= : &t * t = "*$1/=$2;";
    proc %= : &t * t = "*$1%=$2;";
  }
  instance[t in floats] FloatDring[t] {
    fun / : t * t -> t = "$1/$2";
    fun % : t * t -> t = "fmod($1,$2)";
    proc /= : &t * t = "*$1/=$2;";
    proc %= : &t * t = "*$1=fmod($1,$2);";
  }
  instance[t in floats] Real[t] {
    requires Cxx_headers::cmath;
    fun abs: t -> t = "::std::abs($1)";
    fun log10: t -> t = "::std::log10($1)";
    fun sqrt: t -> t = "::std::sqrt($1)";
    fun ceil: t -> t = "::std::ceil($1)";
    fun floor: t -> t = "::std::floor($1)";
    fun trunc: t -> t = "::std::trunc($1)";
    fun embed: int -> t = "(?1)($1)";
    fun atan2: t * t -> t = "::std::atan2($1,$2)";
  }

Floating Numbers.
=================

Operations on Real and Complex numbers.


.. index:: Floatinf(class)
.. index:: Doubleinf(class)
.. index:: Ldoubleinf(class)
.. code-block:: felix

  //[real.flx]
  
  // note: has to be called Fcomplex to avoid clash with class Complex
  
  // Note: ideally we'd use constrained polymorphism for the instances..
  // saves typing it all out so many times
  open class Floatinf
  {
     const FINFINITY : float = "INFINITY" requires C99_headers::math_h;
  }
  
  open class Doubleinf
  {
     const DINFINITY : double = "(double)INFINITY" requires C99_headers::math_h;
  }
  
  open class Ldoubleinf
  {
     const LINFINITY : ldouble = "(long double)INFINITY" requires C99_headers::math_h;
  }
  
  fun isinf[T in reals] : T -> bool = "::std::isinf($1)" requires Cxx_headers::cmath;
  fun isfinite[T in reals] : T -> bool = "::std::isfinite($1)" requires Cxx_headers::cmath;
  fun isnan[T in reals] : T -> bool = "::std::isnan($1)" requires Cxx_headers::cmath;
  
  ctor[T in ints] float : T = "(float)($1)";
  ctor[T in ints] double  : T = "(double)($1)";
  ctor[T in ints] ldouble : T = "(long double)($1)";
  
  ctor float : string = "::std::stof($1)";
  ctor double  : string = "::std::stod($1)";
  ctor ldouble : string = "::std::stold($1)";
  
  
  open Real[float];
  open Real[double];
  open Real[ldouble];
  
Real numbers
============



.. code-block:: felix

  //[real.flx]
  instance[t in reals] Tord[t] {
    fun < : t * t -> bool = "$1<$2";
  }
  
Floating Formats
================


.. index:: float_format(class)
.. index:: fmt(fun)
.. index:: fmt(fun)
.. index:: fmt_default(fun)
.. index:: fmt_fixed(fun)
.. index:: fmt_scientific(fun)
.. index:: xstr(fun)
.. index:: xstr(fun)
.. index:: xstr(fun)
.. code-block:: felix

  //[float_format.flx ]
  //$ Functions to format floating point numbers.
  open class float_format
  {
    //$ Style of formatting.
    //$ default (w,d)    : like C "w.dG" format
    //$ fixed (w,d)      : like C "w.dF" format
    //$ scientific (w,d) : like C "w.dE" format
    variant mode =
      | default of int * int
      | fixed of int * int
      | scientific of int * int
    ;
  
    //$ Format a real number v with format m.
    fun fmt[t in reals] (v:t, m: mode) =>
      match m with
      | default (w,p) => fmt_default(v,w,p)
      | fixed (w,p) => fmt_fixed(v,w,p)
      | scientific(w,p) => fmt_scientific(v,w,p)
      endmatch
    ;
  
    //$ Format a complex number v in x + iy form,
    //$ with format m for x and y.
    fun fmt[t,r with Complex[t,r]] (v:t, m: mode) =>
      match m with
      | default (w,p) => fmt_default(real v,w,p) +"+"+fmt_default(imag v,w,p)+"i"
      | fixed (w,p) => fmt_fixed(real v,w,p)+"+"+fmt_fixed(imag v,w,p)+"i"
      | scientific(w,p) => fmt_scientific(real v,w,p)+"+"+fmt_scientific(imag v,w,p)+"i"
      endmatch
    ;
  
    //$ Format default.
    fun fmt_default[t] : t * int * int -> string="::flx::rtl::strutil::fmt_default($a)" requires package "flx_strutil";
  
    //$ Format fixed.
    fun fmt_fixed[t] : t * int * int -> string="::flx::rtl::strutil::fmt_fixed($a)" requires package "flx_strutil";
  
    //$ Format scientfic.
    fun fmt_scientific[t] : t * int * int -> string="::flx::rtl::strutil::fmt_scientific($a)" requires package "flx_strutil";
  }
  
  instance Str[float] {
    fun xstr: float -> string = "::flx::rtl::strutil::str<#1>($1)" requires package "flx_strutil";
  
    //$ Default format float, also supports nan, +inf, -inf.
    noinline fun str(x:float):string =>
      if isnan x then "nan"
      elif isinf x then
        if x > 0.0f then "+inf" else "-inf" endif
      else xstr x
      endif
    ;
  }
  
  instance Str[double] {
    fun xstr: double -> string = "::flx::rtl::strutil::str<#1>($1)" requires package "flx_strutil";
  
    //$ Default format double, also supports nan, +inf, -inf.
    noinline fun str(x:double):string =>
      if isnan x then "nan"
      elif isinf x then
        if x > 0.0 then "+inf" else "-inf" endif
      else xstr x
      endif
    ;
  }
  
  instance Str[ldouble] {
    fun xstr: ldouble -> string = "::flx::rtl::strutil::str<#1>($1)" requires package "flx_strutil";
  
    //$ Default format long double, also supports nan, +inf, -inf.
    noinline fun str(x:ldouble):string =>
      if isnan x then "nan"
      elif isinf x then
        if x > 0.0l then "+inf" else "-inf" endif
      else xstr x
      endif
    ;
  }
  
  
  
