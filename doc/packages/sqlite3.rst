Package: src/packages/sqlite3.fdoc


========
Database
========

============ =============================
key          file                          
============ =============================
__init__.flx share/lib/std/db/__init__.flx 
sqlite3.flx  share/lib/std/db/sqlite3.flx  
============ =============================

================ ================================
key              file                             
================ ================================
unix_sqlite3.fpc $PWD/src/config/unix/sqlite3.fpc 
win_sqlite3.fpc  $PWD/src/config/win/sqlite3.fpc  
================ ================================

====================== ====================================
key                    file                                 
====================== ====================================
flx_sqlite3_config.hpp share/lib/rtl/flx_sqlite3_config.hpp 
flx_sqlite3.hpp        share/lib/rtl/flx_sqlite3.hpp        
====================== ====================================

================= =========================================
key               file                                      
================= =========================================
sqlite3_01.flx    $PWD/src/test/regress/rt/sqlite_01.flx    
sqlite3_01.expect $PWD/src/test/regress/rt/sqlite_01.expect 
================= =========================================


Synopsis
========



.. code-block:: felix

  //[__init__.flx]
  
  include "std/db/sqlite3";
  
Sqlite3
=======


.. index:: Sqlite3(class)
.. index:: sqlite3_db_t(type)
.. index:: sqlite3_open(gen)
.. index:: sqlite3_close(proc)
.. index:: def(type)
.. index:: sqlite3_exec(gen)
.. index:: sqlite3_exec(gen)
.. index:: sqlite3_errmsg(gen)
.. index:: sqlite3_stmt_t(type)
.. index:: to_sqlite3_result_code(fun)
.. index:: to_sqlite3_type(fun)
.. index:: sqlite3_prepare_v2(gen)
.. index:: sqlite3_column_count(gen)
.. index:: sqlite3_column_name(gen)
.. index:: sqlite3_column_type(gen)
.. index:: sqlite3_column_text(gen)
.. index:: sqlite3_column_double(gen)
.. index:: sqlite3_column_int(gen)
.. index:: sqlite3_column_blob(gen)
.. index:: sqlite3_column_bytes(gen)
.. index:: sqlite3_finalize(gen)
.. index:: sqlite3_prepare_stmt(fun)
.. index:: sqlite3_get_columns(fun)
.. index:: sqlite3_row_iterator(gen)
.. index:: get_int_val(fun)
.. index:: get_double_val(fun)
.. index:: get_text_val(fun)
.. index:: get_stmt(fun)
.. index:: get_next(gen)
.. index:: sqlite3_execute(gen)
.. index:: sqlite3_quote(gen)
.. code-block:: felix

  //[sqlite3.flx]
  
  
  //$ Core Sqlite3 functions and extensions to provide row iterator, simple statement execution, 
  //$ statement preperation and access to sqlite_step statement execution.
  //$
  //$ Iterator example:
  //$ 
  //$
  //$@felix
  //$ var db : sqlite3_db_t;
  //$ var stmt:sqlite3_stmt_t;
  //$ var err = sqlite3_open("multiple_sa.db", &db);
  //$ if err != 0 do
  //$   print "open DB error[abort] ";
  //$   println $ sqlite3_errmsg db;
  //$   goto finish;
  //$ done;
  //$ err = sqlite3_prepare_v2(db, "select * from contact", 21, stmt, "");
  //$ if not err == (caseno SQLITE_OK) then
  //$   { println ("sql error "+str(err)+":"+sqlite3_errmsg(db));goto finish; }
  //$ else {
  //$   var it = sqlite3_row_iterator (stmt);
  //$   var row:ret_val[darray[column_value]];
  //$   while (fun ():bool = { row = it();
  //$              return (match row with |end_of_results[darray[column_value]] =>false |_ => true
  //$              endmatch); }) () do
  //$   var t = match row with 
  //$     | row a =>  ((get_text_val(get(a,0))),(get_text_val(get(a,1))))
  //$     | _ => ("","")
  //$   endmatch;
  //$   print t; endl;
  //$   done
  //$ }
  //$ finish:>
  //$   err = sqlite3_finalize(stmt);
  //$   println(str(err));
  //$   sqlite3_close(db);
  //$@
  
  class Sqlite3 {
    requires package "flx_sqlite3";
  
    //$ Type of a database handle.
    type sqlite3_db_t = "sqlite3*";
  
    //$ Database open.
    gen sqlite3_open : string * &sqlite3_db_t -> int =
      "sqlite3_open($1.c_str(), $2)"
    ;
  
    //$ Database close.
    proc sqlite3_close : sqlite3_db_t = "sqlite3_close($1);";
  
    //$ Type of an exec callback.
    typedef sqlite3_exec_callback_t = 
      address      // client data pointer established by call to sqlite3_exec 
      * int        // number of result columns
      * +(+char)   // column value as text
      * +(+char)   // column name
      --> int
    ;
  
    //$ Quick sql execution using callback.
    //$ arg1: db_handle
    //$ arg2: sql statement.
    //$ arg3: callback function.
    //$ arg4: client data pointer.
    //$ arg5: pointer to error message array.
    //$ result: error code.
    gen sqlite3_exec : sqlite3_db_t * string * sqlite3_exec_callback_t * address * &(+char) -> int =
      "sqlite3_exec($1,$2.c_str(),$3,$4,$5)"
    ;
  
    //$ quick sql execution without data handler callback.
    //$ arg1: db_handle
    //$ arg2: sql statement.
    //$ arg3: pointer to error message array.
    gen sqlite3_exec : sqlite3_db_t * string   * &(+char) -> int =
      "sqlite3_exec($1,$2.c_str(),0,0,$3)"
    ;
  
  
    //$ Error message extractor.
    gen sqlite3_errmsg : sqlite3_db_t -> +char=
      "(char*)sqlite3_errmsg($1)"
    ;
  
    //$ Type of sql statement handle.
    type sqlite3_stmt_t = "sqlite3_stmt*";
  
    //$ Sqlite3 return codes.
    enum sqlite3_result_codes {
       SQLITE_OK         =   0,   /* Successful result */
       SQLITE_ERROR      =   1,   /* SQL error or missing database */
       SQLITE_INTERNAL   =   2,   /* Internal logic error in SQLite */
       SQLITE_PERM       =   3,   /* Access permission denied */
       SQLITE_ABORT      =   4,   /* Callback routine requested an abort */
       SQLITE_BUSY       =   5,   /* The database file is locked */
       SQLITE_LOCKED     =   6,   /* A table in the database is locked */
       SQLITE_NOMEM      =   7,   /* A malloc() failed */
       SQLITE_READONLY   =   8,   /* Attempt to write a readonly database */
       SQLITE_INTERRUPT  =   9,   /* Operation terminated by sqlite3_interrupt()*/
       SQLITE_IOERR      =  10,   /* Some kind of disk I/O error occurred */
       SQLITE_CORRUPT    =  11,   /* The database disk image is malformed */
       SQLITE_NOTFOUND   =  12,   /* Unknown opcode in sqlite3_file_control() */
       SQLITE_FULL       =  13,   /* Insertion failed because database is full */
       SQLITE_CANTOPEN   =  14,   /* Unable to open the database file */
       SQLITE_PROTOCOL   =  15,   /* Database lock protocol error */
       SQLITE_EMPTY      =  16,   /* Database is empty */
       SQLITE_SCHEMA     =  17,   /* The database schema changed */
       SQLITE_TOOBIG     =  18,   /* String or BLOB exceeds size limit */
       SQLITE_CONSTRAINT =  19,   /* Abort due to constraint violation */
       SQLITE_MISMATCH   =  20,   /* Data type mismatch */
       SQLITE_MISUSE     =  21,   /* Library used incorrectly */
       SQLITE_NOLFS      =  22,   /* Uses OS features not supported on host */
       SQLITE_AUTH       =  23,   /* Authorization denied */
       SQLITE_FORMAT     =  24,   /* Auxiliary database format error */
       SQLITE_RANGE      =  25,   /* 2nd parameter to sqlite3_bind out of range */
       SQLITE_NOTADB     =  26,   /* File opened that is not a database file */
       SQLITE_ROW        =  100,  /* sqlite3_step() has another row ready */
       SQLITE_DONE       =  101,  /* sqlite3_step() has finished executing */
       SQLITE_UNK_RESULT = 999
    }
  
    //$ Conversion from int result to named return codes.
    fun to_sqlite3_result_code: int -> sqlite3_result_codes =
       |0 => SQLITE_OK        
       |1 => SQLITE_ERROR     
       |2 => SQLITE_INTERNAL  
       |3 => SQLITE_PERM      
       |4 => SQLITE_ABORT     
       |5 => SQLITE_BUSY      
       |6 => SQLITE_LOCKED    
       |7 => SQLITE_NOMEM     
       |8 => SQLITE_READONLY  
       |9 => SQLITE_INTERRUPT 
       |10 => SQLITE_IOERR    
       |11 => SQLITE_CORRUPT  
       |12 => SQLITE_NOTFOUND 
       |13 => SQLITE_FULL     
       |14 => SQLITE_CANTOPEN 
       |15 => SQLITE_PROTOCOL 
       |16 => SQLITE_EMPTY    
       |17 => SQLITE_SCHEMA   
       |18 => SQLITE_TOOBIG   
       |19 => SQLITE_CONSTRAINT
       |20 => SQLITE_MISMATCH 
       |21 => SQLITE_MISUSE 
       |22 => SQLITE_NOLFS  
       |23 => SQLITE_AUTH   
       |24 => SQLITE_FORMAT 
       |25 => SQLITE_RANGE  
       |26 => SQLITE_NOTADB 
       |100 => SQLITE_ROW   
       |101 => SQLITE_DONE 
       | _   => SQLITE_UNK_RESULT;
  
    //$ Tag names for Sqlite3 data types.
    enum sqlite3_types {
      SQLITE_INTEGER  = 1,
      SQLITE_FLOAT    = 2,
      SQLITE_TEXT     = 3,
      SQLITE_BLOB     = 4,
      SQLITE_NULL     = 5,
      SQLITE_UNK_TYPE = 999
    }
  
    instance Eq[sqlite3_result_codes]  {
      //$ Allow checking for specific return codes.
      fun ==: sqlite3_result_codes * sqlite3_result_codes -> bool = "$1==$2";
    }
    open Eq[sqlite3_result_codes];
  
    //$ Conversion from int type to named Sqlite3 data type.
    fun to_sqlite3_type: int -> sqlite3_types =
      |1 => SQLITE_INTEGER
      |2 => SQLITE_FLOAT 
      |4 => SQLITE_BLOB
      |5 => SQLITE_NULL
      |3 => SQLITE_TEXT
      | _ => SQLITE_UNK_TYPE;
  
       
    //$ Prepare an sqlite3 statement for execution.
    gen sqlite3_prepare_v2: sqlite3_db_t * string * int * sqlite3_stmt_t *string -> int =
    "sqlite3_prepare_v2($1,$2.c_str(),$3,&$4,NULL)";
   
    //$ Execute one step of the prepared statement.
    noinline gen sqlite3_step: sqlite3_stmt_t -> int = "sqlite3_step($1)";
   
    //$ Determine the number of columns (field) a statement will process.
    gen sqlite3_column_count: sqlite3_stmt_t -> int = "sqlite3_column_count($1)";
  
    //$ Determine the name of the n'th column to be processed.
    gen sqlite3_column_name: sqlite3_stmt_t*int -> string = "sqlite3_column_name($1,$2)";
  
    //$ Determine the type of the n'th column to be processed.
    gen sqlite3_column_type: sqlite3_stmt_t*int->int = "sqlite3_column_type($1,$2)";
  
    //$ Fetch the value of a text field.
    gen sqlite3_column_text: sqlite3_stmt_t*int->string = "(char *)(sqlite3_column_text($1,$2))";
  
    //$ Fetch the value of a double field.
    gen sqlite3_column_double: sqlite3_stmt_t*int->double = "sqlite3_column_double($1,$2)";
  
    //$ Fetch the value of a int field.
    gen sqlite3_column_int: sqlite3_stmt_t*int->int = "sqlite3_column_int($1,$2)";
  
    //$ Fetch the value of a blob field.
    gen sqlite3_column_blob: sqlite3_stmt_t*int->&byte = "(unsigned char *)sqlite3_column_blob($1,$2)";
    
    //$ Fetch the number of bytes of a field.
    gen sqlite3_column_bytes: sqlite3_stmt_t*int -> int = "sqlite3_column_bytes($1,$2)";
  
    //$ Finish up with stepping a statement.
    //$ Releases associated resources.
    //$ The statement handle becomes invalid afterwards.
    gen sqlite3_finalize: sqlite3_stmt_t -> int = "sqlite3_finalize($1)";
  
    //$ A unified type to fetch a field value.
    variant column_value =
       |int_val of int
       |double_val of double
       |text_val of string
       |byte_val of int*&byte
       |null_val;
  
    //$ A unified result of a statement.
    variant ret_val[t] =
       |row of t
       |row_fail of sqlite3_result_codes*string
       |end_of_results;
  
    //$ A unified result code.
    variant result_code[t] =
      | qry_ok of t
      | qry_fail of sqlite3_result_codes*string;
  
    //$ Unified preparation of a query.
    fun sqlite3_prepare_stmt (db:sqlite3_db_t,query:string):result_code[sqlite3_stmt_t] = {
      var stmt:sqlite3_stmt_t;
      return match to_sqlite3_result_code ( sqlite3_prepare_v2(db, query, int(len query), stmt, "")) with
        | #SQLITE_OK =>  qry_ok stmt
        | c     => qry_fail[sqlite3_stmt_t] (c,str(sqlite3_errmsg(db)))
      endmatch;
    }
  
    //$ Fetch all the columns of a query at once.
    //$ Return them in a darray.
    fun sqlite3_get_columns (stmt:sqlite3_stmt_t):darray[column_value] = {
      val n = sqlite3_column_count(stmt);
      val results = darray[column_value]( size n,null_val);
      for var i:int in 0 upto n - 1 do
         var v = match to_sqlite3_type( sqlite3_column_type(stmt, i) ) with
                   | #SQLITE_TEXT    => text_val (sqlite3_column_text(stmt, i))
                   | #SQLITE_INTEGER     => int_val (sqlite3_column_int(stmt, i))
                   | #SQLITE_FLOAT   => double_val (sqlite3_column_double(stmt, i))
                   | #SQLITE_BLOB    => byte_val (sqlite3_column_bytes(stmt,i),
                                                sqlite3_column_blob(stmt, i)) 
                   | #SQLITE_NULL => null_val
                 endmatch;
         set(results,i,v );
      done;
      return results;
    }
  
  
    //$ A stream iterator which returns successive rows of a table.
    gen sqlite3_row_iterator (stmt:sqlite3_stmt_t) () :ret_val[darray[column_value]]  = {
      again:> 
        var result_code = to_sqlite3_result_code$ sqlite3_step(stmt);
        if result_code == SQLITE_BUSY do goto again; done;
         match result_code  with
          | #SQLITE_DONE => {val p=sqlite3_finalize(stmt);}(); yield end_of_results[darray[column_value]];
          | #SQLITE_ROW  => yield ( row ( sqlite3_get_columns stmt) );
        //| #SQLITE_BUSY => { Faio::sleep (Faio::sys_clock,0.05); goto again; end_of_results[darray[column_value]];}
           | v =>  {val p=sqlite3_finalize stmt;}(); yield  end_of_results[darray[column_value]];
        endmatch;
        goto again;
        yield end_of_results[darray[column_value]]; 
    }
  
  
    //$ Get the int value out of a int typed field.
    //$ Throws match failure if the field isn't an int type.
    fun get_int_val: column_value->int = | int_val v => v;
  
    //$ Get the double value out of a double typed field.
    //$ Throws match failure if the field isn't a double type.
    fun get_double_val:  column_value->double = | double_val v => v;
  
    //$ Get the text value out of a text typed field.
    //$ Throws match failure if the field isn't a text type.
    fun get_text_val:  column_value->string = | text_val v => v;
  
    //$ Get the statement handle out of a return code.
    fun get_stmt: result_code[sqlite3_stmt_t]-> sqlite3_stmt_t = | qry_ok v => v;
  
    //$ Get the next row from an row iterator.
    gen get_next ( iter:()->ret_val[darray[column_value]],row:&ret_val[darray[column_value]]):bool = { 
      row <- iter();
       return (match *row with 
                | #end_of_results =>false 
                | #row_fail =>false 
                | _ => true
              endmatch); 
    }
  
    //$ Execute an prepared statement.
    gen sqlite3_execute (stmt:sqlite3_stmt_t) :bool  = {     
        val v= match to_sqlite3_result_code$ sqlite3_step(stmt)  with
          | #SQLITE_BUSY => sqlite3_execute(stmt)
          | #SQLITE_DONE => true
          | _           => false
        endmatch;
        val n = sqlite3_finalize stmt;
        return v;
    }
  
    header """
      std::string sqlite3_quote_helper(const char *str) {
        const char * val = sqlite3_mprintf("%q",str);
        std::string ret = std::string(val);
        sqlite3_free((char *)val);
        return ret;
      }
    """;
  
    //$ Quote a string for use in a query.
    gen sqlite3_quote: string->string = "sqlite3_quote_helper($1.c_str())";
  
  }
  
  


Test Example
============


.. code-block:: felix

  //[sqlite3_01.flx]
  include "std/db/sqlite3";
  
  open Sqlite3;
  
  fun subscript: + (+char) * int -> +char = "$1[$2]";
  
  cfun eh(data:address, ncols:int, values: + (+char), names: + (+char)):int =
  {
    var ii:int = 0;
    while ii<ncols do
      print$ str names.[ii] + "=" + str values.[ii];
      if ii<ncols- 1  do print ", ";  done;
      ++ii;
    done;
    println "";
    return 0;
  }
  
  proc run(db:sqlite3_db_t) {
    sql :=
      "drop table if exists fred;",
      "create table fred (name, address);",
      "insert into fred values('joe','wigram');",
      "insert into fred values('max','gpr');",
      "insert into fred values('lee','wax');",
      "insert into fred values('henry','pollen');",
      "select all name,address from fred;",
      ""
    ;
    var usr: address =  address c"user pointer";
    var errm: +char =  C_hack::cast[+char] c""; // cast const ptr to non-const
  
    var i = 0;
    var p = sql.i;
    while p != "" do
      println p;
      val cb : sqlite3_exec_callback_t = eh;
      res := sqlite3_exec(db,p,cb,usr,&errm);
      if res !=0 do
        println$ "exec DB error[abort]: " + errm;
        return;
      done;
      ++i;
      p = sql.i;
    done;
  }
  
  println "Hello";
  var db : sqlite3_db_t;
  err := sqlite3_open("mydb.db", &db);
  if err != 0 do
    print "open DB error[abort] ";
    println $ sqlite3_errmsg db;
    goto finish;
  done;
  
  run(db);
  
  finish:>
    sqlite3_close(db);


.. code-block:: text

  Hello
  drop table if exists fred;
  create table fred (name, address);
  insert into fred values('joe','wigram');
  insert into fred values('max','gpr');
  insert into fred values('lee','wax');
  insert into fred values('henry','pollen');
  select all name,address from fred;
  name=joe, address=wigram
  name=max, address=gpr
  name=lee, address=wax
  name=henry, address=pollen


Config Data
===========


.. code-block:: fpc

  //[unix_sqlite3.fpc]
  provides_dlib: -lflx_sqlite3_dynamic
  provides_slib: -lflx_sqlite3_static
  includes: '"flx_sqlite3.hpp"'
  macros: BUILD_SQLITE3
  build_includes: build/release/share/lib/rtl
  library: flx_sqlite3
  srcdir: src/sqlite3
  src: sqlite3\.c


.. code-block:: fpc

  //[win_sqlite3.fpc]
  provides_dlib: /DEFAULTLIB:flx_sqlite3_dynamic
  provides_slib: /DEFAULTLIB:flx_sqlite3_static
  includes: "<flx_sqlite3.hpp>"
  macros: BUILD_SQLITE3
  build_includes: build/release/share/lib/rtl
  library: flx_sqlite3
  srcdir: src/sqlite3
  src: sqlite3\.c


.. code-block:: cpp

  //[flx_sqlite3_config.hpp]
  #ifndef __FLX_SQLITE3_CONFIG_H__
  #define __FLX_SQLITE3_CONFIG_H__
  #include "flx_rtl_config.hpp"
  #ifdef BUILD_SQLITE3
  #define SQLITE3_EXTERN FLX_EXPORT
  #else
  #define SQLITE3_EXTERN FLX_IMPORT
  #endif
  #endif
  #define SQLITE_API SQLITE3_EXTERN


.. code-block:: cpp

  //[flx_sqlite3.hpp]
  #ifndef _FLX_SQLITE3_HPP
  #define _FLX_SQLITE3_HPP
  #include "flx_sqlite3_config.hpp"
  #include "sqlite3/sqlite3.h"
  #endif


