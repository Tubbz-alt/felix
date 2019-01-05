Package: src/packages/strings.fdoc


=======
Strings
=======


============ ==================================
key          file                               
============ ==================================
__init__.flx share/lib/std/strings/__init__.flx 
string.flx   share/lib/std/strings/string.flx   
============ ==================================


String handling
===============



.. code-block:: felix

  //[__init__.flx]
  include "std/strings/string";
  include "std/strings/cstring";
  include "std/strings/ustr";
  
Strings
=======

We have three string like things.  :code:`cstring` is just 
an alias for a NTBS (Null Terminated Byte String).
The workhorse  :code:`string` type based on C++ string.

A  :code:`ustring` is a unicode representation using a 32 bit unsigned integer as
the character base.
This type is deprecated, to be repalced by C++11 unicode string type.



.. index:: Str(class)
.. index:: str(fun)
.. index:: Repr(class)
.. index:: repr(fun)
.. index:: Show(class)
.. code-block:: felix

  //[string.flx]
  typedef cstring = +char;
  type string = "::std::basic_string<char>" 
    requires Cxx_headers::string,
    header '#include "flx_serialisers.hpp"',
    encoder "::flx::gc::generic::string_encoder",
    decoder "::flx::gc::generic::string_decoder"
  ;
  typedef strings = typesetof (string);
  
  class Str [T] {
    virtual fun str: T -> string;
  }
  
  class Repr [T with Str[T]] {
    virtual fun repr (t:T) : string => str t;
  }
  
  class Show [T] {
    inherit Str[T];
    inherit Repr[T];
  }
  
  
Equality and total ordering
---------------------------



.. index:: String(class)
.. code-block:: felix

  //[string.flx]
  instance[t in strings] Eq[t] {
    fun == : t * t -> bool = "$1==$2";
  }
  instance[t in strings] Tord[t] {
    fun < : t * t -> bool = "$1<$2";
  }
  
  class String
  {
    inherit Eq[string];
  
    inherit Tord[string];
  
Equality of  :code:`string` and  :code:`char`
---------------------------------------------



.. code-block:: felix

  //[string.flx]
    fun == (s:string, c:char) => len s == 1uz and s.[0] == c;
    fun == (c:char, s:string) => len s == 1uz and s.[0] == c;
    fun != (s:string, c:char) => len s != 1uz or s.[0] != c;
    fun != (c:char, s:string) => len s != 1uz or s.[0] != c;
  
Append to  :code:`string` object
--------------------------------



.. code-block:: felix

  //[string.flx]
    proc  += : &string * string = "$1->append($2:assign);";
    proc  += : &string * +char = "$1->append($2:assign);";
    proc  += : &string * char = "*$1 += $2;";
    proc  += : &string * &string = "$1->append(*$2);";
  
Length of  :code:`string`
-------------------------



.. index:: len(fun)
.. index:: len(fun)
.. code-block:: felix

  //[string.flx]
    // we need to cast to an int so that c++ won't complain
    fun len: string -> size = "$1.size()";
    fun len: &string -> size = "$1->size()";
  
String concatenation.
---------------------



.. code-block:: felix

  //[string.flx]
    fun + : string * string -> string = "$1+$2";
    fun + : string * carray[char] -> string = "$1+$2";
    fun + : string * char -> string = "$1+$2";
    fun + : char * string -> string = "$1+$2";
    //fun + : string * int -> string = "$1+::flx::rtl::i18n::utf8($2:assign)" is add requires package "flx_i18n";
    fun + ( x:string,  y: int) => x + str y;
  
    // may be a bit risky!
    // IT WAS: interferes with "hello" + list ("world","blah"): 
    // is this a string or a list of strings?
    //fun + [T with Str[T]] (x:string, y:T) => x + str y;
  
Repetition of  :code:`string` or  :code:`char`
----------------------------------------------



.. code-block:: felix

  //[string.flx]
    fun * : string * int -> string = "::flx::rtl::strutil::mul($1:assign,$2:assign)" requires package "flx_strutil";
    fun * : char * int -> string = "::std::string($2:assign,$1:assign)";
  
Application of  :code:`string` to  :code:`string` or  :code:`int` is concatenation
----------------------------------------------------------------------------------



.. index:: apply(fun)
.. index:: apply(fun)
.. code-block:: felix

  //[string.flx]
    fun apply (x:string, y:string):string => x + y;
    fun apply (x:string, y:int):string => x + y;
  
Construct a char from first byte of a  :code:`string`.
------------------------------------------------------

Returns nul char (code 0) if the string is empty.


.. index:: char(ctor)
.. code-block:: felix

  //[string.flx]
    ctor char (x:string) => x.[0];
Constructors for  :code:`string`
--------------------------------



.. index:: string(ctor)
.. index:: string(ctor)
.. index:: string(ctor)
.. index:: utf8(fun)
.. code-block:: felix

  //[string.flx]
    ctor string (c:char) => ""+c;
    ctor string: +char = "::std::string($1:assign)";
    ctor string: +char  * !ints = "::std::string($1:assign,$2:assign)";
    fun utf8: int -> string = "::flx::rtl::i18n::utf8($1)" requires package "flx_i18n";
  
Substrings
----------



.. index:: subscript(fun)
.. index:: copyfrom(fun)
.. index:: copyto(fun)
.. index:: substring(fun)
.. index:: subscript(fun)
.. index:: apply(fun)
.. index:: subscript(fun)
.. index:: store(proc)
.. code-block:: felix

  //[string.flx]
    fun subscript: string * !ints -> char =
      "::flx::rtl::strutil::subscript($1:assign,$2:assign)" requires package "flx_strutil";
    fun copyfrom: string * !ints -> string =
      "::flx::rtl::strutil::substr($1:assign,$2:assign,$1:postfix.size())" requires package "flx_strutil";
    fun copyto: string * !ints -> string =
      "::flx::rtl::strutil::substr($1:assign,0,$2:assign)" requires package "flx_strutil";
    fun substring: string * !ints * !ints -> string =
      "::flx::rtl::strutil::substr($1:assign,$2:assign,$3:assign)" requires package "flx_strutil";
  
    fun subscript (x:string, s:slice[int]):string =>
      match s with
      | #Slice_all => substring (x, 0, x.len.int)
      | Slice_from (start) => copyfrom (x, start)
      | Slice_to_incl (end) => copyto (x, end + 1)
      | Slice_to_excl (end) => copyto (x, end)
      | Slice_range_incl (start, end) => substring (x, start, end + 1)
      | Slice_range_excl (start, end) => substring (x, start, end)
      | Slice_from_counted (start, count) => substring (x,start, start + count)
      | Slice_one (index) => string x.[index]
      endmatch
    ;
    fun apply (s:slice[int], x:string) => subscript (x,s);
  
    fun subscript (x:string, gs:gslice[int]):string = {
      var r = "";
      match gs with
      | GSlice s => r = subscript(x,s);
      | GSSList gsl =>
        // this should be faster cause it cats a list of string which
        // is linear in the number of strings
        var sl = Empty[string]; 
        for gs in gsl perform sl = subscript (x,gs) + sl;
        r = sl.rev.(cat "");
      | _ => 
        for i in gs perform r += x.[i];
      endmatch; 
      return r;
    }
   
    proc store: &string * !ints * char = "(*$1)[$2] = $3;";
  
Map a string  :code:`char` by  :code:`char`
-------------------------------------------



.. index:: map(fun)
.. code-block:: felix

  //[string.flx]
    fun map (f:char->char) (var x:string): string = {
      if len x > 0uz do
        for var i in 0uz upto (len x) - 1uz do
          store(&x, i, f x.[i]);
        done
      done
      return x;
    }
  
STL string functions
--------------------

These come in two flavours: the standard C++ operations
which return  :code:`stl_npos` on failure, and a more Felix
like variant which uses an  :code:`option` type.


.. index:: stl_npos(const)
.. index:: stl_find(fun)
.. index:: stl_find(fun)
.. index:: stl_find(fun)
.. index:: stl_find(fun)
.. index:: stl_find(fun)
.. index:: stl_find(fun)
.. index:: find(fun)
.. index:: find(fun)
.. index:: find(fun)
.. index:: find(fun)
.. index:: find(fun)
.. index:: find(fun)
.. index:: stl_rfind(fun)
.. index:: stl_rfind(fun)
.. index:: stl_rfind(fun)
.. index:: stl_rfind(fun)
.. index:: stl_rfind(fun)
.. index:: stl_rfind(fun)
.. index:: rfind(fun)
.. index:: rfind(fun)
.. index:: rfind(fun)
.. index:: rfind(fun)
.. index:: rfind(fun)
.. index:: rfind(fun)
.. index:: stl_find_first_of(fun)
.. index:: stl_find_first_of(fun)
.. index:: stl_find_first_of(fun)
.. index:: stl_find_first_of(fun)
.. index:: stl_find_first_of(fun)
.. index:: stl_find_first_of(fun)
.. index:: find_first_of(fun)
.. index:: find_first_of(fun)
.. index:: find_first_of(fun)
.. index:: find_first_of(fun)
.. index:: find_first_of(fun)
.. index:: find_first_of(fun)
.. index:: stl_find_first_not_of(fun)
.. index:: stl_find_first_not_of(fun)
.. index:: stl_find_first_not_of(fun)
.. index:: stl_find_first_not_of(fun)
.. index:: stl_find_first_not_of(fun)
.. index:: stl_find_first_not_of(fun)
.. index:: find_first_not_of(fun)
.. index:: find_first_not_of(fun)
.. index:: find_first_not_of(fun)
.. index:: find_first_not_of(fun)
.. index:: find_first_not_of(fun)
.. index:: find_first_not_of(fun)
.. index:: stl_find_last_of(fun)
.. index:: stl_find_last_of(fun)
.. index:: stl_find_last_of(fun)
.. index:: stl_find_last_of(fun)
.. index:: stl_find_last_of(fun)
.. index:: stl_find_last_of(fun)
.. index:: find_last_of(fun)
.. index:: find_last_of(fun)
.. index:: find_last_of(fun)
.. index:: find_last_of(fun)
.. index:: find_last_of(fun)
.. index:: find_last_of(fun)
.. index:: stl_find_last_not_of(fun)
.. index:: stl_find_last_not_of(fun)
.. index:: stl_find_last_not_of(fun)
.. index:: stl_find_last_not_of(fun)
.. index:: stl_find_last_not_of(fun)
.. index:: stl_find_last_not_of(fun)
.. index:: find_last_not_of(fun)
.. index:: find_last_not_of(fun)
.. index:: find_last_not_of(fun)
.. index:: find_last_not_of(fun)
.. index:: find_last_not_of(fun)
.. index:: find_last_not_of(fun)
.. code-block:: felix

  //[string.flx]
    const stl_npos: size = "::std::string::npos";
  
    fun stl_find: string * string -> size = "$1.find($2)" is cast;
    fun stl_find: string * string * size -> size = "$1.find($2,$3)" is cast;
    fun stl_find: string * +char -> size = "$1.find($2)" is cast;
    fun stl_find: string * +char * size -> size = "$1.find($2,$3)" is cast;
    fun stl_find: string * char -> size = "$1.find($2)" is cast;
    fun stl_find: string * char * size -> size = "$1.find($2,$3)" is cast;
  
    fun find (s:string, e:string) : opt[size] => match stl_find (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find (s:string, e:string, i:size) : opt[size] => match stl_find (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find (s:string, e:+char) : opt[size] => match stl_find (s, e) with | i when i== stl_npos => None[size] | i => Some i endmatch;
    fun find (s:string, e:+char, i:size) : opt[size] => match stl_find (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find (s:string, e:char) : opt[size] => match stl_find (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find (s:string, e:char, i:size) : opt[size] => match stl_find (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
  
    fun stl_rfind: string * string -> size = "$1.rfind($2)";
    fun stl_rfind: string * string * size -> size = "$1.rfind($2,$3)";
    fun stl_rfind: string * +char-> size = "$1.rfind($2)";
    fun stl_rfind: string * +char * size -> size = "$1.rfind($2,$3)";
    fun stl_rfind: string * char -> size = "$1.rfind($2)";
    fun stl_rfind: string * char * size -> size = "$1.rfind($2,$3)";
  
    fun rfind (s:string, e:string) : opt[size] => match stl_rfind (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun rfind (s:string, e:string, i:size) : opt[size] => match stl_rfind (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun rfind (s:string, e:+char) : opt[size] => match stl_rfind (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun rfind (s:string, e:+char, i:size) : opt[size] => match stl_rfind (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun rfind (s:string, e:char) : opt[size] => match stl_rfind (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun rfind (s:string, e:char, i:size) : opt[size] => match stl_rfind (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
  
    fun stl_find_first_of: string * string -> size = "$1.find_first_of($2)";
    fun stl_find_first_of: string * string * size -> size = "$1.find_first_of($2,$3)";
    fun stl_find_first_of: string * +char -> size = "$1.find_first_of($2)";
    fun stl_find_first_of: string * +char * size -> size = "$1.find_first_of($2,$3)";
    fun stl_find_first_of: string * char -> size = "$1.find_first_of($2)";
    fun stl_find_first_of: string * char * size -> size = "$1.find_first_of($2,$3)";
  
    fun find_first_of (s:string, e:string) : opt[size] => match stl_find_first_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_of (s:string, e:string, i:size) : opt[size] => match stl_find_first_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_of (s:string, e:+char) : opt[size] => match stl_find_first_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_of (s:string, e:+char, i:size) : opt[size] => match stl_find_first_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_of (s:string, e:char) : opt[size] => match stl_find_first_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_of (s:string, e:char, i:size) : opt[size] => match stl_find_first_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
  
    fun stl_find_first_not_of: string * string -> size = "$1.find_first_not_of($2)";
    fun stl_find_first_not_of: string * string * size -> size = "$1.find_first_not_of($2,$3)";
    fun stl_find_first_not_of: string * +char -> size = "$1.find_first_not_of($2)";
    fun stl_find_first_not_of: string * +char * size -> size = "$1.find_first_not_of($2,$3)";
    fun stl_find_first_not_of: string * char -> size = "$1.find_first_not_of($2)";
    fun stl_find_first_not_of: string * char * size -> size = "$1.find_first_not_of($2,$3)";
  
    fun find_first_not_of (s:string, e:string) : opt[size] => match stl_find_first_not_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_not_of (s:string, e:string, i:size) : opt[size] => match stl_find_first_not_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_not_of (s:string, e:+char) : opt[size] => match stl_find_first_not_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_not_of (s:string, e:+char, i:size) : opt[size] => match stl_find_first_not_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_not_of (s:string, e:char) : opt[size] => match stl_find_first_not_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_first_not_of (s:string, e:char, i:size) : opt[size] => match stl_find_first_not_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
  
    fun stl_find_last_of: string * string -> size = "$1.find_last_of($2)";
    fun stl_find_last_of: string * string * size -> size = "$1.find_last_of($2,$3)";
    fun stl_find_last_of: string * +char -> size = "$1.find_last_of($2)";
    fun stl_find_last_of: string * +char * size -> size = "$1.find_last_of($2,$3)";
    fun stl_find_last_of: string * char -> size = "$1.find_last_of($2)";
    fun stl_find_last_of: string * char * size -> size = "$1.find_last_of($2,$3)";
  
    fun find_last_of (s:string, e:string) : opt[size] => match stl_find_last_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_of (s:string, e:string, i:size) : opt[size] => match stl_find_last_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_of (s:string, e:+char) : opt[size] => match stl_find_last_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_of (s:string, e:+char, i:size) : opt[size] => match stl_find_last_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_of (s:string, e:char) : opt[size] => match stl_find_last_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_of (s:string, e:char, i:size) : opt[size] => match stl_find_last_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
  
    fun stl_find_last_not_of: string * string -> size = "$1.find_last_not_of($2)";
    fun stl_find_last_not_of: string * string * size -> size = "$1.find_last_not_of($2,$3)";
    fun stl_find_last_not_of: string * +char -> size = "$1.find_last_not_of($2)";
    fun stl_find_last_not_of: string * +char * size -> size = "$1.find_last_not_of($2,$3)";
    fun stl_find_last_not_of: string * char -> size = "$1.find_last_not_of($2)";
    fun stl_find_last_not_of: string * char * size -> size = "$1.find_last_not_of($2,$3)";
  
    fun find_last_not_of (s:string, e:string) : opt[size] => match stl_find_last_not_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_not_of (s:string, e:string, i:size) : opt[size] => match stl_find_last_not_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_not_of (s:string, e:+char) : opt[size] => match stl_find_last_not_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_not_of (s:string, e:+char, i:size) : opt[size] => match stl_find_last_not_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_not_of (s:string, e:char) : opt[size] => match stl_find_last_not_of (s, e) with | i when i == stl_npos => None[size] | i => Some i endmatch;
    fun find_last_not_of (s:string, e:char, i:size) : opt[size] => match stl_find_last_not_of (s, e, i) with | i when i == stl_npos => None[size] | i => Some i endmatch;
  
    
Construe  :code:`string` as set of  :code:`char`
------------------------------------------------



.. code-block:: felix

  //[string.flx]
    instance Set[string,char] {
      fun \in (c:char, s:string) => stl_find (s,c) != stl_npos;
    }
    
Construe  :code:`string` as stream of  :code:`char`
---------------------------------------------------



.. code-block:: felix

  //[string.flx]
    instance Iterable[string, char] {
      gen iterator(var x:string) () = {
        for var i in 0 upto x.len.int - 1 do yield Some (x.[i]); done
        return None[char];
      }
    }
    inherit Streamable[string,char];
  
Test if a string has given prefix or suffix
-------------------------------------------



.. index:: prefix(fun)
.. index:: suffix(fun)
.. index:: startswith(fun)
.. index:: endswith(fun)
.. index:: startswith(fun)
.. index:: endswith(fun)
.. code-block:: felix

  //[string.flx]
    fun prefix(arg:string,key:string)=>
      arg.[to len key]==key
    ;
  
    fun suffix (arg:string,key:string)=>
      arg.[-key.len to]==key
    ;
  
  
    fun startswith (x:string) (e:string) : bool => prefix (x,e);
  
    // as above: slices are faster
    fun endswith (x:string) (e:string) : bool => suffix (x,e);
  
    fun startswith (x:string) (e:char) : bool => x.[0] == e;
    fun endswith (x:string) (e:char) : bool => x.[-1] == e;
  
Trim off specified prefix or suffix or both
-------------------------------------------



.. index:: ltrim(fun)
.. index:: rtrim(fun)
.. index:: trim(fun)
.. code-block:: felix

  //[string.flx]
    fun ltrim (x:string) (e:string) : string =>
      if startswith x e then
        x.[e.len.int to]
      else
        x
      endif
    ;
  
    fun rtrim (x:string) (e:string) : string =>
      if endswith x e then
        x.[to x.len.int - e.len.int]
      else
        x
      endif
    ;
  
    fun trim (x:string) (e:string) : string => ltrim (rtrim x e) e;
  
Strip characters from left, right, or both end of a string.
-----------------------------------------------------------



.. index:: lstrip(fun)
.. index:: rstrip(fun)
.. index:: strip(fun)
.. index:: lstrip(fun)
.. index:: rstrip(fun)
.. index:: strip(fun)
.. code-block:: felix

  //[string.flx]
    fun lstrip (x:string, e:string) : string =
    {
      if len x > 0uz do
        for var i in 0uz upto len x - 1uz do
          var found = false;
          for var j in 0uz upto len e - 1uz do
            if x.[i] == e.[j] do
              found = true;
            done
          done
  
          if not found do
            return x.[i to];
          done
        done;
      done
      return '';
    }
  
    fun rstrip (x:string, e:string) : string =
    {
      if len x > 0uz do
        for var i in len x - 1uz downto 0uz do
          var found = false;
          for var j in 0uz upto len e - 1uz do
            if x.[i] == e.[j] do
              found = true;
            done
          done
  
          if not found do
            return x.[to i.int + 1];
          done
        done
      done
      return '';
    }
  
    fun strip (x:string, e:string) : string => lstrip(rstrip(x, e), e);
  
    fun lstrip (x:string) : string => lstrip(x, " \t\n\r\f\v");
    fun rstrip (x:string) : string => rstrip(x, " \t\n\r\f\v");
    fun strip (x:string) : string => lstrip$ rstrip x;
  
Justify string contents
-----------------------



.. index:: ljust(fun)
.. index:: rjust(fun)
.. code-block:: felix

  //[string.flx]
    fun ljust(x:string, width:int) : string =>
      if x.len.int >= width
        then x
        else x + (' ' * (width - x.len.int))
      endif
    ;
  
    fun rjust(x:string, width:int) : string =>
      if x.len.int >= width
        then x
        else (' ' * (width - x.len.int)) + x
      endif
    ;
  
Split a string into a list on given separator
---------------------------------------------



.. index:: split(fun)
.. index:: rev_split(fun)
.. index:: split(fun)
.. index:: rev_split(fun)
.. index:: split(fun)
.. index:: rev_split(fun)
.. index:: split_first(fun)
.. index:: respectful_split(fun)
.. index:: respectful_split(fun)
.. code-block:: felix

  //[string.flx]
    fun split (x:string, d:char): List::list[string] => List::rev (rev_split (x,d));
  
    fun rev_split (x:string, d:char): List::list[string] = {
      fun aux (x:string,y:List::list[string]) =>
        match find (x, d) with
        | #None => Cons (x, y)
        | Some n => aux$ x.[n+1uz to], List::Cons (x.[to n],y)
        endmatch
      ;
      return aux$ x, List::Empty[string];
    }
  
    fun split (x:string, d:string): List::list[string] => List::rev (rev_split (x,d));
  
    fun rev_split (x:string, d:string): List::list[string] = {
      fun aux (pos:size,y:List::list[string]) =>
        match stl_find_first_of (x, d, pos) with
        | $(stl_npos) => List::Cons (x.[pos to],y)
        | n => aux$ (n+1uz), List::Cons (x.[pos to n],y)
        endmatch
      ;
      return aux$ 0uz, List::Empty[string];
    }
  
    fun split (x:string, d:+char): List::list[string] => List::rev (rev_split (x,d));
  
    fun rev_split (x:string, d:+char): List::list[string] = {
      fun aux (x:string,y:List::list[string]) =>
        match find_first_of (x, d) with
        | #None => List::Cons (x, y)
        | Some n => aux$ x.[n+1uz to], List::Cons (x.[to n],y)
        endmatch
      ;
      return aux$ x, List::Empty[string];
    }
  
    fun split_first (x:string, d:string): opt[string*string] =>
      match find_first_of (x, d) with
      | #None => None[string*string]
      | Some n => Some (x.[to n],substring(x,n+1uz,(len x)))
      endmatch
    ;
  
  
    //$ Split a string on whitespace but respecting
    //$ double quotes, single quotes, and slosh escapes.
    // leading and trailing space is removed. Embedded
    // multiple spaces cause a single split.
    class RespectfulParser {
      variant quote_action_t = 
        | ignore-quote
        | keep-quote
        | drop-quote
      ; 
      variant dquote_action_t = 
        | ignore-dquote
        | keep-dquote
        | drop-dquote
      ; 
      variant escape_action_t = 
        | ignore-escape
        | keep-escape
        | drop-escape
      ; 
      typedef action_t = (quote:quote_action_t, dquote:dquote_action_t, escape:escape_action_t);
  
      variant mode_t = | copying | skipping | quote | dquote | escape-copying | escape-quote | escape-dquote;
      typedef state_t = (mode:mode_t, current:string, parsed: list[string] );
  
      noinline fun respectful_parse (action:action_t) (var state:state_t) (var s:string) : state_t = 
      {
        var mode = state.mode;
        var current = state.current;
        var result = Empty[string];
  
        noinline proc handlecopying(ch:char) {
          if ch == char "'" do
            match action.quote with
            | #ignore-quote => 
              current += ch;
            | #keep-quote =>
              current += ch;
              mode = quote;
            | #drop-quote =>
              mode = quote;
            endmatch;
          elif ch == char '"' do
            match action.dquote with
            | #ignore-dquote => 
              current += ch;
            | #keep-dquote =>
              current += ch;
              mode = dquote;
            | #drop-dquote =>
              mode = dquote;
            endmatch;
          elif ch == char '\\' do
            match action.escape with
            | #ignore-escape => 
              current += ch;
            | #keep-escape =>
              current += ch;
              mode = escape-copying;
            | #drop-escape =>
              mode = escape-copying;
            endmatch;
          elif ord ch <= ' '.char.ord  do // can't happen if called from skipping
            result += current;
            current = "";
            mode = skipping;
          else
            current += ch;
            mode = copying;
          done
        }
  
        for ch in s do 
          match mode with
          | #copying => handlecopying ch;
          | #quote =>
            if ch == char "'" do
              match action.quote with
              | #ignore-quote => 
                assert false;
                //current += ch;
              | #keep-quote =>
                current += ch;
                mode = copying;
              | #drop-quote =>
                mode = copying;
              endmatch;
            elif ch == char "\\" do
              match action.escape with
              | #ignore-escape => 
                current += ch;
              | #keep-escape =>
                current += ch;
                mode = escape-quote;
              | #drop-escape =>
                mode = escape-quote;
              endmatch;
            else
              current += ch;
            done 
  
          | #dquote =>
            if ch == char '"' do
              match action.dquote with
              | #ignore-dquote => 
                assert false;
                //current += ch;
              | #keep-dquote =>
                current += ch;
                mode = copying;
              | #drop-dquote =>
                mode = copying;
              endmatch;
            elif ch == char "\\" do
              match action.escape with
              | #ignore-escape => 
                current += ch;
              | #keep-escape =>
                current += ch;
                mode = escape-dquote;
              | #drop-escape =>
                mode = escape-dquote;
              endmatch;
            else
              current += ch;
            done 
  
          | #escape-copying =>
             current += ch;
             mode = copying;
  
          | #escape-quote =>
             current += ch;
             mode = quote;
  
          | #escape-dquote =>
             current += ch;
             mode = dquote;
  
          | #skipping =>
            if ord ch > ' '.char.ord  do
              handlecopying ch;
            done
          endmatch;
        done
        return (mode=mode, current=current, parsed=state.parsed + result);
      }
    }
    
    // simplified one shot parser.
    // ignores mismatched quotes and backslashes.
    fun respectful_split (action:RespectfulParser::action_t) (s:string) : list[string] = 
    {
      var state = RespectfulParser::respectful_parse
        action 
        (
          mode=RespectfulParser::skipping, 
          current="", 
          parsed=Empty[string]
        ) 
        s
      ;
      // ignore mismatched quotes and backslashes.
      match state.mode with 
      | #skipping => ;
      | _ => &state.parsed <- state.parsed + state.current;
      endmatch;
      return state.parsed;
   
    }
  
    fun respectful_split (s:string) : list[string] =>
      respectful_split (
        quote=RespectfulParser::keep-quote, 
        dquote=RespectfulParser::keep-dquote, 
        escape=RespectfulParser::keep-escape
      ) 
      s
    ; 
  
    // OO version of the parser.
    object respectfulParser (action:RespectfulParser::action_t) = {
      var state = (mode=RespectfulParser::skipping, current="", parsed=Empty[string]);
      method proc parse (s:string) {
        state = RespectfulParser::respectful_parse action state s;
      }
      method fun get_parsed () => state.parsed;
    }
  
erase, insert or replace substrings
-----------------------------------



.. index:: erase(proc)
.. index:: insert(proc)
.. index:: replace(proc)
.. index:: erase(fun)
.. index:: insert(fun)
.. index:: replace(fun)
.. code-block:: felix

  //[string.flx]
    // Note: pos, length!
    //$ mutators
    proc erase: &string * size * size = "$1->erase($2,$3);";
    proc insert: &string * size * string = "$1->insert($2,$3);";
    proc replace: &string * size * size * string = "$1->replace($2,$3,$4);";
  
    //$ functional
    fun erase: string * size * size -> string = "::std::string($1).erase($2,$3)";
    fun insert: string * size * string -> string = "::std::string($1).insert($2,$3)";
    fun replace: string * size * size * string -> string = "::std::string($1).replace($2,$3,$4)";
  
  
search and replace
------------------

Search and replace by string.


.. index:: search_and_replace(fun)
.. index:: search_and_replace(fun)
.. index:: search_and_replace(fun)
.. code-block:: felix

  //[string.flx]
    fun search_and_replace (x:string, var spos:size, s:string, r:string) : string =
    {
      val m = s.len;
      var o = x.[to spos];
      var n = (x,s,spos).stl_find;
      while n != stl_npos do
        o+=x.[spos to n]+r;
        spos = n+m;
        n = (x,s,spos).stl_find.size;
      done
      o+=x.[spos to];
      return o;
    }
    fun search_and_replace (x:string, s:string, r:string) : string => search_and_replace (x,0uz,s,r);
  
    fun search_and_replace (vs:list[string * string]) (var v:string) = {
      match k,b in vs do
        v = search_and_replace (v,k,b);
      done
      return v;
    }
  
Regexp search and replace
-------------------------

Uses Google RE2 engine.


.. index:: subst(fun)
.. index:: search_and_replace(fun)
.. code-block:: felix

  //[string.flx]
    // Replace \0 \1 \2 etc in s with text from v
    fun subst(s:string, v:varray[StringPiece]): string =
    {
    //println$ "Subst " + s +" with " + str v;
       enum mode_t {cp, ins};
       var b = "";
       var mode=cp;
       var j = 0;
       var count = 0;
       for var i in 0 upto s.len.int - 1 do
         match mode with
         | #cp => 
           if s.[i] == char "\\" do 
             mode = ins; 
             j=0; count = 0; 
           else 
            b += s.[i]; 
           done
         | #ins =>
           if s.[i] in "0123456789" do
             j = j * 10 + ord(s.[i]) - ord (char "0");
             ++count;
           else
             if count == 0 do
               b += "\\";
             elif j < v.len.int do
               b+= str v.stl_begin.j;
             done
             // adjacent insertion?
             if s.[i] == char "\\" do
               j=0; count=0;
             else
               mode = cp;
               b += s.[i]; 
             done
           done
         endmatch;
       done
       // run off end
       match mode with
       | #cp => ;
       | #ins =>
         if count == 0 do
           b += "\\";
         elif j < v.len.int do
           b+= str v.j;
         done
       endmatch;
       return b;
    }
    // Search for regex, replace by r with \0 \1 \2 etc replace by match groups.
    fun search_and_replace (x:string, var spos: size, re:Re2::RE2, r:string) : string =
    {
      var ngroups = re.NumberOfCapturingGroups + 1;
      var v = varray[StringPiece]$ (ngroups+1).size, StringPiece "";
      var o = x.[to spos];             // initial substring
      var sp = StringPiece(x);
      var base : +char = sp.data;      // base pointer of char array
      while Re2::Match(re, sp, spos.int, UNANCHORED, v.stl_begin, v.len.int) do
        var mpos = size(v.0.data - base);  // start of match
        o+= x.[spos to mpos];          // copy upto start of match
        o+= subst(r,v);                // copy replacement
        spos = mpos + v.0.len;       // advance over match
      done
      o+=x.[spos to];                  // rest of string
      return o;
    }
Parse string to numeric type
----------------------------



.. index:: atoi(fun)
.. index:: atol(fun)
.. index:: atoll(fun)
.. index:: atof(fun)
.. code-block:: felix

  //[string.flx]
    fun atoi: string -> int = "::std::atoi($1:postfix.c_str())"  requires Cxx_headers::cstdlib;
    fun atol: string -> long = "::std::atol($1:postfix.c_str())"  requires Cxx_headers::cstdlib;
    fun atoll: string -> long = "::std::atoll($1:postfix.c_str())"  requires Cxx_headers::cstdlib;
    fun atof: string -> double = "::std::atof($1:postfix.c_str())"  requires Cxx_headers::cstdlib;
  
Reserve store
-------------



.. index:: reserve(proc)
.. code-block:: felix

  //[string.flx]
    proc reserve: &string * !ints = "$1->reserve($2);";
  
Fetch underlying cstring.
-------------------------



.. index:: _unsafe_cstr(fun)
.. index:: stl_begin(fun)
.. index:: stl_end(fun)
.. index:: cstr(fun)
.. code-block:: felix

  //[string.flx]
    // safely returns a malloc()'d copy, not garbage collected 
    fun _unsafe_cstr: string -> +char = "::flx::rtl::strutil::flx_cstr($1)" is atom;
  
    // partially unsafe because the string could be modified.
    fun stl_begin: &string -> +char = "((char*)$1->c_str())" is atom;
    fun stl_end: &string -> +char = "((char*)($1->c_str()+$1->size()))" is atom;
  
    // this operation returns a char pointer to GC managed storage
    fun cstr (var s:string) => s.varray[char].stl_begin;
  
Polymorphic vsprintf hack
-------------------------



.. index:: vsprintf(fun)
.. index:: vsprintf(fun)
.. code-block:: felix

  //[string.flx]
    fun vsprintf[t]: +char  * t -> string =
      "::flx::rtl::strutil::flx_asprintf($1,$2)" requires package "flx_strutil"
    ;
  
    fun vsprintf[t]: string * t -> string =
      "::flx::rtl::strutil::flx_asprintf(const_cast<char*>($1.c_str()),$2)" requires package "flx_strutil"
    ;
  
Case translation
----------------



.. index:: toupper(fun)
.. index:: tolower(fun)
.. code-block:: felix

  //[string.flx]
    // Convert all characters to upper case  
    fun toupper(s:string):string => map (toupper of char) s;
    // Convert all characters to lower case
    fun tolower(s:string):string => map (tolower of char) s;
  }
  
  
Transation to string
--------------------


.. index:: str(fun)
.. index:: str(fun)
.. index:: repr(fun)
.. code-block:: felix

  //[string.flx]
  
  instance Str[string] {
    fun str (s:string) : string => s;
  }
  
  instance Str[+char] {
    fun str: +char -> string = '::flx::rtl::strutil::atostr($1)' requires package "flx_strutil";
  }
  
  instance Repr[string] {
    fun repr (x:string) : string = {
      var o = "'";
      if len x > 0uz do
        for var i in 0uz upto (String::len x) - 1uz do
          o += repr x.[i];
        done
      done
      return o + "'";
    }
  }
  
  open[T in strings] Show[T];
  open Set[string,char];
  
  
