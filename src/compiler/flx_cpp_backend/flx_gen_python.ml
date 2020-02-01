open List

open Flx_bbdcl
open Flx_beta
open Flx_bexe
open Flx_bexpr
open Flx_bparameter
open Flx_btype
open Flx_cexpr
open Flx_ctorgen
open Flx_ctypes
open Flx_display
open Flx_egen
open Flx_exceptions
open Flx_label
open Flx_list
open Flx_maps
open Flx_mtypes2
open Flx_name
open Flx_ogen
open Flx_options
open Flx_pgen
open Flx_print
open Flx_types
open Flx_typing
open Flx_unify
open Flx_util
open Flx_gen_helper


let gen_python_module modname syms bsym_table bifaces =
  let pychk acc elt = match elt with
  | BIFACE_export_python_fun (sr,index,name) ->
    let class_name = cpp_instance_name syms bsym_table index [] in
    let loc = Flx_srcref.short_string_of_src sr in
    let entry = name, class_name, loc in
    entry :: acc
  | _ -> acc
  in
  let funs = fold_left pychk [] bifaces in
  match funs with
  | [] -> ""
  | funs -> 
      "// Python 3 module definition for " ^ modname ^ "\n" ^
      "static PyMethodDef " ^ modname ^ "_methods [] = {\n" ^
      cat "" (rev_map (fun (export_name, symbol_name, loc) ->
      "  {" ^ "\"" ^ export_name ^ "\", " ^ symbol_name ^ 
      ", METH_VARARGS, \""^loc^"\"},\n"
      ) funs) ^ 
      "  {NULL, NULL, 0, NULL}\n" ^
      "};\n" ^
      "static PyModuleDef " ^ modname ^"_module = {\n" ^
        "PyModuleDef_HEAD_INIT,       // m_base\n"^
        "\"" ^ modname ^ "\",                  // m_name\n" ^
        "\"" ^ modname ^ " generated by Felix \", // m_doc\n" ^
        "-1,                          // m_size\n" ^          
        modname ^ "_methods,          // m_methods\n" ^
        "0,                           // m_reload\n" ^                                      
        "0,                           // m_traverse\n" ^                                      
        "0,                           // m_clear\n" ^                                      
        "0                           // m_free\n" ^                                      
      "};\n" ^
(* Note: Python uses PyMODINIT_FUNC, however it gets the exports wrong
  so the compiler is now doing the visibility control directly
*)
      "extern \"C\" FLX_EXPORT PyObject *PyInit_" ^ modname ^ "()" ^
      " { return PyModule_Create(&" ^ modname ^ "_module);}\n"


