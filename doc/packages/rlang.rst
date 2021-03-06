Package: src/packages/rlang.fdoc


===============
R language DSSL
===============

========== =========================
key        file                      
========== =========================
rcore.flx  share/lib/rlang/rcore.flx 
rtest.flx  $PWD/rtest.flx            
========== =========================


R core
======

Work in progress implementing R interpreter.



.. index:: Rcore(class)
.. index:: str(fun)
.. code-block:: felix

  //[rtest.flx]
  library Rlang {
  class Rcore {
  
  typedef Rtype = (`Rlogical_t| `Rinteger_t | `Rdouble_t | `Rcomplex_t | `Rcharacter_t);
  instance Str[Rtype] {
    fun str (x:Rtype) : string => match x with
    | `Rlogical_t () => "logical"
    | `Rinteger_t () => "integer"
    | `Rdouble_t () => "double"
    | `Rcomplex_t () => "complex"
    | `Rcharacter_t () => "character"
    ;
  }
  typedef Rlogical_v = ( `Rtrue | `Rfalse | `Rlogical_NA );
  typedef Rinteger_v = ( `Rinteger of int | `Rinteger_NA );
  typedef Rdouble_v = ( `Rdouble of double | `Rdouble_NA );
  typedef Rcomplex_v = ( `Rcomplex of dcomplex | `Rcomplex_NA);
  typedef Rcharacter_v = ( `Rcharacter of string | `Rcharacter_NA);
  
  typedef Rscalar_v = ( Rlogical_v | Rinteger_v | Rdouble_v | Rcomplex_v | Rcharacter_v); 
  typedef Rbasic_vector_v = (
    `Rlogical_x of varray[Rlogical_v] | 
    `Rinteger_x of varray[Rinteger_v] | 
    `Rdouble_x of varray[Rdouble_v] | 
    `Rcomplex_x of varray[Rcomplex_v] | 
    `Rcharacter_x of varray[Rcharacter_v] | 
    `Rraw_x of varray[byte]  
  );
  typedef Robject_v = (
    `Rnull | 
    Rbasic_vector_v | 
    `Rlist of varray[Robject_v] |  // heterogenous
    `Rsymbol of string |            // variable name 
    `Rexternal_pointer of address
  );
  
  }}
  
  include "rlang/rcore";
  open Rlang;
  open Rcore;
  
  println$ "Hello R";
  var x = #`Rlogical_t :>> Rtype;
  println$ x;
  
  
