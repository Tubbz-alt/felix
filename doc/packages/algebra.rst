Package: src/packages/algebra.fdoc

============= ======================================
key           file                                   
============= ======================================
init.flx      share/lib/std/algebra/__init__.flx     
set.flx       share/lib/std/algebra/set.flx          
container.flx share/lib/std/algebra/container.flx    
equiv.flx     share/lib/std/algebra/equiv.flx        
pord.flx      share/lib/std/algebra/partialorder.flx 
tord.flx      share/lib/std/algebra/totalorder.flx   
group.flx     share/lib/std/algebra/group.flx        
ring.flx      share/lib/std/algebra/ring.flx         
trig.flx      share/lib/std/algebra/trig.flx         
real.flx      share/lib/std/algebra/real.flx         
complex.flx   share/lib/std/algebra/complex.flx      
integer.flx   share/lib/std/algebra/integer.flx      
bits.flx      share/lib/std/algebra/bits.flx         
sequence.flx  share/lib/std/algebra/sequence.flx     
monad.flx     share/lib/std/algebra/monad.flx        
============= ======================================

==========================
Core Algebraic Structures.
==========================


Synopsis.
=========




.. code-block:: felix

  //[init.flx]
  include "std/algebra/predicate";        // in logic.fdoc
  include "std/algebra/set";              // in algebra.fdoc
  include "std/algebra/container";        // in algebra.fdoc
  include "std/algebra/equiv";            // in algebra.fdoc
  include "std/algebra/partialorder";     // in algebra.fdoc  
  include "std/algebra/totalorder";       // in algebra.fdoc
  include "std/algebra/sequence";         // in algebra.fdoc
  include "std/algebra/group";            // in algebra.fdoc
  include "std/algebra/ring";             // in algebra.fdoc
  include "std/algebra/bits";             // in algebra.fdoc
  include "std/algebra/integer";          // in algebra.fdoc
  include "std/algebra/trig";             // in algebra.fdoc
  include "std/algebra/real";             // in algebra.fdoc
  include "std/algebra/complex";          // in algebra.fdoc
  include "std/algebra/monad";            // in algebra.fdoc
  
Description.
============

In this section we provide abstract definitions of some basic
mathematical stuctures which will be used to specify
operations on numeric types.

We use polymorphic classes to do this. A class is introduced by
the  :code:`class` keyword followed by its name, then a list
of type variables in square brackets. Then the body is
presented enclosed in curly braces.

Two kinds of specification are allowed in a polymorphic class:
function definitions and assertions.


Functions.
----------

There are two kinds of function definitions. A function
or procedure specified with the adjective  :code:`virtual`
may have a specialisation provided in an instance declaration.
Virtual functions may have definitions, in which case the
definition is merely a default. It can be replaced in a specialising
instance. However the definition should be taken as a semantic
specification which the specialisation should adhere too.

The set of virtual functions of a polymorphic class is known
as the <em>basis</em> of the class.

A non-virtual function can be defined in terms of virtual functions
and other non-virtual functions.  Non virtual functions cannot be 
specialised by the programmer.  Instead, they are automatically specialised 
by the system for an instance.


Assertions
----------

A polymorphic class may also contain assertions. These are
function like specifications which specify semantic constraints.

An  :code:`axiom` specifies a basic assertion, it specifies a class property in 
terms of relations between the class functions. Since Felix only
supports first order assertional logic, higher order semantics
must be specified in comments.

If a class contains virtual functions with definitions,
the definition is also considered as axiomatic.


The set of all axioms, including those in comments,
is known as the <em>assertional basis</em> or <em>semantic specification</em>
of the class.  Additionally some reductions may be or imply an
extension of the semantic basis.

A  :code:`lemma` is an assertion which can be derived from the semantic
specifications by logical reasoning. In particular, lemmas in
principle should be self-evident, simple and useful and able
to be deduced by an automatic theorm proving program.

A  :code:`theorem` is a more complicated derived assertion,
which would be too hard to prove with an automatic theorem
prover. Instead, it should be derivable with a proof 
assistant (such as Coq), given various unspecified 
strategies, tactics and hints.




Sets.
=====

A <em>set</em> is any type with a membership predicate :math:`\in` 
spelled  :code:`\in`. You can also use function  :code:`mem`. The parser
also maps  :code:`in` to operator  :code:`\in`.

We also provide a reversed form :math:`\owns`  spelled  :code:`\owns`,
and negated forms :math:`ni`  spelled  :code:`\ni` or  :code:`\notin`.

Three combinators are provided as well, :math:`\cap`  spelled  :code:`cap`
provides intersection, :math:`\cup`  spelled  :code:`\cup` provides
the usual set union, and :math:`\setminus`  spelled  :code:`\setminus`
the asymmetic set difference or subtraction.

Note that sets are not necessarily finite.


.. index:: Set(class)
.. index:: mem(fun)
.. code-block:: felix

  //[set.flx]
  // note: eq is not necessarily required for a membership test
  // for example: string member of regexp doesn't require
  // string equality
  // Set need not be finite (example regexp again)
  // A list is a set, despite the duplications
  class Set[c,t] {
    fun mem (elt:t, container:c):bool => elt \in container;
    virtual fun \in : t * c-> bool;
    fun \owns (container:c, elt:t) => elt \in container;
    fun \ni (container:c, elt:t) => elt \in container;
    fun \notin (elt:t, container:c) => not (elt \in container);
  
    fun \cup[c2 with Set[c2,t]] 
      (x:c, y:c2) => 
      { e : t | e \in x or e \in y }
    ;
  
    fun \cap[c2 with Set[c2,t]] 
      (x:c, y:c2) => 
      { e : t | e \in x and e \in y }
    ;
  
    fun \setminus[c2 with Set[c2,t]] 
      (x:c, y:c2) => 
      { e : t | e \in x and e \notin y }
    ;
  }
  
Set forms.
==========

A  :code:`set_form` is a record type with a single 
member  :code:`has_elt` which returns true if it's argument
is intended as a member of some particular set.

We construe a set_form as a Set by providing an
instance.

A set_form is basically just the membership predicate remodelled
as a noun by encapsulating the predicate in a closure and
thereby abstracting it.


.. code-block:: felix

  //[set.flx]
  interface set_form[T] { has_elt: T -> bool; }
  
  instance[T] Set[set_form[T], T] {
    fun \in (elt:T, s:set_form[T]) => s.has_elt elt;
  }
  open[T] Set[set_form[T],T];
  
  // INVERSE image of a set under a function
  // For a function f: t -> t2, an element e
  // is in a restriction of the domain t if its
  // image in t2 is in the specified set.
  fun invimg[t,c2,t2 with Set[c2,t2]] 
    (f:t->t2, x:c2) : set_form[t] =>
    { e : t | (f e) \in x }
  ;
  
Cartesian Product of set_forms.
-------------------------------

This uses some advanced instantiation technology
to allow you to define the cartesian product of a
sequence of sets using the infix TeX operator :math:`\otimes` 
which is spelled  :code:`\otimes`. There's also a left associative
binary operator :math:`\times`  spelled  :code:`\times`.


.. code-block:: felix

  //[set.flx]
  
  fun \times[U,V] (x:set_form[U],y:set_form[V]) => 
    { u,v : U * V | u \in x and v \in y }
  ;
  
  fun \otimes[U,V] (x:set_form[U],y:set_form[V]) => 
    { u,v : U * V | u \in x and v \in y }
  ;
  
  fun \otimes[U,V,W] (head:set_form[U], tail:set_form[V*W]) =>
    { u,v,w : U * V * W | u \in head and (v,w) \in tail }
  ;
  
  fun \otimes[NH,OH,OT] (head:set_form[NH], tail:set_form[OH**OT]) =>
    { h,,(oh,,ot) : NH ** (OH ** OT) | h \in head and (oh,,ot) \in tail }
  ;
  
Containers.
===========



.. index:: Container(class)
.. index:: len(fun)
.. index:: empty(fun)
.. code-block:: felix

  //[container.flx]
  // roughly, a finite Set
  class Container [c,v]
  {
    inherit Set[c,v];
    virtual fun len: c -> size;
    fun \Vert (x:c) => len x;
    virtual fun empty(x: c): bool => len x == size(0);
  }
  
  
Orders
======


Equivalence Relation.
---------------------

An `equivalence <https://en.wikipedia.org/wiki/Equivalence_relation>`_ relation 
is a `reflexive <https://en.wikipedia.org/wiki/Reflexive_relation>`_, 
`symmetric <https://en.wikipedia.org/wiki/Symmetric_relation>`_,
`transitive <https://en.wikipedia.org/wiki/Transitive_relation>`_
relation. It is one of the most fundamental concepts in
mathematics. One can show that for any set :math:`S` , for any
element :math:`s \in  S` , the subset :math:`\lbrack s\rbrack`  of :math:`S`  
consisting of all elements equivalent to :math:`s`  are also
equivalent to each other, and not equivalent to any other
element outside that set.

Therefore, every equivalence relation on a set :math:`S`  specifies 
a `partition <https://en.wikipedia.org/wiki/Partition_of_a_set>`_ 
of :math:`S`  which is a set of subsets of :math:`S` 
known as `equivalence classes <https://en.wikipedia.org/wiki/Equivalence_class>`_, 
or just plain classes,
such that no two classes have a common
intersection, and the union of the classes spans the whole set.

In other words a partition consists of 
a `disjoint union <https://en.wikipedia.org/wiki/Disjoint_union>`_
of subsets.

The most fundamential relation in computing which is required
to be an equivalence relation is the equality operator.
In particular, it allows us to have distinct encodings of
a value, but still consider them equal semantically,
and to provide an operational measure of that equivalence.

As a simple example, consider that the rational numbers
:math:`1/2`  and :math:`2/4`  have distinct encodings but none-the-less
are semantically equivalent.

An online reference on `Wikibooks <http://en.wikibooks.org/wiki/Abstract_Algebra/Equivalence_relations_and_congruence_classes>`_



.. index:: Eq(class)
.. index:: eq(fun)
.. index:: ne(fun)
.. code-block:: felix

  //[equiv.flx]
  // equality: technically, equivalence relation
  class Eq[t] {
    virtual fun == : t * t -> bool;
    virtual fun != (x:t,y:t):bool => not (x == y);
  
    axiom reflex(x:t): x == x;
    axiom sym(x:t, y:t): (x == y) == (y == x);
    axiom trans(x:t, y:t, z:t): x == y and y == z implies x == z;
  
    fun eq(x:t, y:t)=> x == y;
    fun ne(x:t, y:t)=> x != y;
    fun \ne(x:t, y:t)=> x != y;
    fun \neq(x:t, y:t)=> x != y;
  }
  
  
Partial Order
-------------

A proper `partial order <https://en.wikipedia.org/wiki/Partially_ordered_set>`_ 
:math:`\subset`  spelled  :code:`\subset`
is a transitive, 
`antisymmetric <https://en.wikipedia.org/wiki/Antisymmetric_relation>`_ 
`irreflexive <https://en.wikipedia.org/wiki/Reflexive_relation>`_ relation.

We also provide an improper operator :math:`\subseteq`  
spelled  :code:`\subseteq` which is transitive, antisymmetric,
and reflexive, for which either the partial order
or equivalence operator  :code:`==` applies.

The choice of operators is motivated by the canonical
exemplar of subset containment relations.


.. index:: Pord(class)
.. code-block:: felix

  //[pord.flx]
  // partial order
  class Pord[t]{
    inherit Eq[t];
    virtual fun \subset: t * t -> bool;
    virtual fun \supset(x:t,y:t):bool =>y \subset x;
    virtual fun \subseteq(x:t,y:t):bool => x \subset y or x == y;
    virtual fun \supseteq(x:t,y:t):bool => x \supset y or x == y;
  
    fun \subseteqq(x:t,y:t):bool => x \subseteq y;
    fun \supseteqq(x:t,y:t):bool => x \supseteq y;
  
    fun \nsubseteq(x:t,y:t):bool => not (x \subseteq y);
    fun \nsupseteq(x:t,y:t):bool => not (x \supseteq y);
    fun \nsubseteqq(x:t,y:t):bool => not (x \subseteq y);
    fun \nsupseteqq(x:t,y:t):bool => not (x \supseteq y);
  
    fun \supsetneq(x:t,y:t):bool => x \supset y;
    fun \supsetneqq(x:t,y:t):bool => x \supset y;
    fun \supsetneq(x:t,y:t):bool => x \supset y;
    fun \supsetneqq(x:t,y:t):bool => x \supset y;
  
    axiom trans(x:t, y:t, z:t): \subset(x,y) and \subset(y,z) implies \subset(x,z);
    axiom antisym(x:t, y:t): \subset(x,y) or \subset(y,x) or x == y;
    axiom reflex(x:t, y:t): \subseteq(x,y) and \subseteq(y,x) implies x == y;
  }
Bounded Partial Order
---------------------

A partial order may bave an upper or lower bound known as the supremum
and infimum, respectively. If these values are in the type, they are called
the maximum and minimum, respectively.



.. index:: UpperBoundPartialOrder(class)
.. index:: upperbound(fun)
.. index:: LowerBoundPartialOrder(class)
.. index:: lowerbound(fun)
.. index:: BoundPartialOrder(class)
.. code-block:: felix

  //[pord.flx]
  class UpperBoundPartialOrder[T] {
    inherit Pord[T];
    virtual fun upperbound: 1 -> T;
  }
  class LowerBoundPartialOrder[T] {
    inherit Pord[T];
    virtual fun lowerbound: 1 -> T;
  }
  class BoundPartialOrder[T] {
    inherit LowerBoundPartialOrder[T];
    inherit UpperBoundPartialOrder[T];
  }
  
  
  
Total Order
-----------

A `total order <https://en.wikipedia.org/wiki/Total_order>`_ is a 
partial order with a `totality law <https://en.wikipedia.org/wiki/Total_relation>`_.

However we do not derive it from our partial order because
we use different comparison operators. Here we use the
standard ascii art comparison operators commonly found
in programming languages along with the more beautiful
TeX operators used in mathematical papers.

The spelling of the TeX operators can be found by
holding the mouse over the symbol briefly.



.. index:: Tord(class)
.. index:: lt(fun)
.. index:: gt(fun)
.. index:: le(fun)
.. index:: ge(fun)
.. index:: max(fun)
.. index:: min(fun)
.. code-block:: felix

  //[tord.flx]
  // total order
  class Tord[t]{
    inherit Eq[t];
    // defined in terms of <, argument order swap, and boolean negation
  
    // less
    virtual fun < : t * t -> bool;
    fun lt (x:t,y:t): bool=> x < y;
    fun \lt (x:t,y:t): bool=> x < y;
    fun \lneq (x:t,y:t): bool=> x < y;
    fun \lneqq (x:t,y:t): bool=> x < y;
  
  
    axiom trans(x:t, y:t, z:t): x < y and y < z implies x < z;
    axiom antisym(x:t, y:t): x < y or y < x or x == y;
    axiom reflex(x:t, y:t): x < y and y <= x implies x == y;
    axiom totality(x:t, y:t): x <= y or y <= x;
  
  
    // greater
    fun >(x:t,y:t):bool => y < x;
    fun gt(x:t,y:t):bool => y < x;
    fun \gt(x:t,y:t):bool => y < x;
    fun \gneq(x:t,y:t):bool => y < x;
    fun \gneqq(x:t,y:t):bool => y < x;
  
    // less equal
    fun <= (x:t,y:t):bool => not (y < x);
    fun le (x:t,y:t):bool => not (y < x);
    fun \le (x:t,y:t):bool => not (y < x);
    fun \leq (x:t,y:t):bool => not (y < x);
    fun \leqq (x:t,y:t):bool => not (y < x);
    fun \leqslant (x:t,y:t):bool => not (y < x);
  
  
    // greater equal
    fun >= (x:t,y:t):bool => not (x < y);
    fun ge (x:t,y:t):bool => not (x < y);
    fun \ge (x:t,y:t):bool => not (x < y);
    fun \geq (x:t,y:t):bool => not (x < y);
    fun \geqq (x:t,y:t):bool => not (x < y);
    fun \geqslant (x:t,y:t):bool => not (x < y);
  
    // negated, strike-through
    fun \ngtr (x:t,y:t):bool => not (x < y);
    fun \nless (x:t,y:t):bool => not (x < y);
  
    fun \ngeq (x:t,y:t):bool => x < y;
    fun \ngeqq (x:t,y:t):bool => x < y;
    fun \ngeqslant (x:t,y:t):bool => x < y;
  
    fun \nleq (x:t,y:t):bool => not (x <= y);
    fun \nleqq (x:t,y:t):bool => not (x <= y);
    fun \nleqslant (x:t,y:t):bool => not (x <= y);
    
  
    // maxima and minima
    fun max(x:t,y:t):t=> if x < y then y else x endif;
    fun \vee(x:t,y:t) => max (x,y);
  
    fun min(x:t,y:t):t => if x < y then x else y endif;
    fun \wedge(x:t,y:t):t => min (x,y);
  
  
  }
Bounded Total Orders.
---------------------



.. index:: UpperBoundTotalOrder(class)
.. index:: maxval(fun)
.. index:: LowerBoundTotalOrder(class)
.. index:: minval(fun)
.. index:: BoundTotalOrder(class)
.. code-block:: felix

  //[tord.flx]
  class UpperBoundTotalOrder[T] {
    inherit Tord[T];
    virtual fun maxval: 1 -> T = "::std::numeric_limits<?1>::max()";
  }
  class LowerBoundTotalOrder[T] {
    inherit Tord[T];
    virtual fun minval: 1 -> T = "::std::numeric_limits<?1>::min()";
  }
  class BoundTotalOrder[T] {
    inherit LowerBoundTotalOrder[T];
    inherit UpperBoundTotalOrder[T];
  }
  
  
Sequences
---------

Sequences are discrete total orders.


.. index:: ForwardSequence(class)
.. index:: succ(fun)
.. index:: pre_incr(proc)
.. index:: post_incr(proc)
.. index:: BidirectionalSequence(class)
.. index:: pred(fun)
.. index:: pre_decr(proc)
.. index:: post_decr(proc)
.. index:: RandomSequence(class)
.. index:: advance(fun)
.. index:: BoundForwardSequence(class)
.. index:: BoundBidirectionalSequence(class)
.. index:: BoundRandomSequence(class)
.. code-block:: felix

  //[sequence.flx]
  
  // Forward iterable
  class ForwardSequence[T] {
    inherit Tord[T];
    virtual fun succ: T -> T;
    virtual proc pre_incr: &T;
    virtual proc post_incr: &T;
  }
  
  // Bidirectional
  class BidirectionalSequence[T] {
    inherit ForwardSequence[T];
    virtual fun pred: T -> T;
    virtual proc pre_decr: &T;
    virtual proc post_decr: &T;
  }
  
  // Bounded Random access totally ordered
  // int should be any integer type really .. fix later
  class RandomSequence[T] {
    inherit BidirectionalSequence[T];
    virtual fun advance : int * T -> T;
  }
  
  // Bounded totally ordered forward iterable
  class BoundForwardSequence[T] {
    inherit ForwardSequence[T];
    inherit UpperBoundTotalOrder[T];
  }
  
  // Bounded totally ordered bidirectional
  class BoundBidirectionalSequence[T] {
    inherit BidirectionalSequence[T];
    inherit BoundTotalOrder[T];
  }
  
  // Bounded Random access totally ordered
  class BoundRandomSequence[T] {
    inherit RandomSequence[T];
    inherit BoundBidirectionalSequence[T];
  }
  
Groupoids.
==========



Approximate Additive Group
--------------------------

An approximate additive group is a type for which
there is a symmetric binary addition operator, a zero element,
and for which there is an additive inverse or negation operator.

It is basically an additive group without the associativity
requirement, and is intended to apply to floating point
numbers.

Note we use the  :code:`inherit` statement to include
the functions from class  :code:`Eq`.

.. index:: FloatAddgrp(class)
.. index:: zero(fun)
.. index:: neg(fun)
.. index:: prefix_plus(fun)
.. index:: add(fun)
.. index:: plus(fun)
.. index:: sub(fun)
.. index:: pluseq(proc)
.. index:: minuseq(proc)
.. code-block:: felix

  //[group.flx]
  //$ Additive symmetric float-approximate group, symbol +.
  //$ Note: associativity is not assumed.
  class FloatAddgrp[t] {
    inherit Eq[t];
    virtual fun zero: unit -> t;
    virtual fun + : t * t -> t;
    virtual fun neg : t -> t;
    virtual fun prefix_plus : t -> t = "$1";
    virtual fun - (x:t,y:t):t => x + -y;
    virtual proc += (px:&t,y:t) { px <- *px + y; }
    virtual proc -= (px:&t,y:t) { px <- *px - y; }
  
    reduce id (x:t): x+zero() => x;
    reduce id (x:t): zero()+x => x;
    reduce inv(x:t): x - x => zero();
    reduce inv(x:t): - (-x) => x;
    axiom sym (x:t,y:t): x+y == y+x;
  
    fun add(x:t,y:t)=> x + y;
    fun plus(x:t)=> +x;
    fun sub(x:t,y:t)=> x - y;
    proc pluseq(px:&t, y:t) {  += (px,y); }
    proc  minuseq(px:&t, y:t) { -= (px,y); }
  }

Additive Group
--------------

A proper additive group is derived from  :code:`FloatAddgrp`
with associativity added.


.. index:: Addgrp(class)
.. code-block:: felix

  //[group.flx]
  //$ Additive symmetric group, symbol +.
  class Addgrp[t] {
    inherit FloatAddgrp[t];
    axiom assoc (x:t,y:t,z:t): (x + y) + z == x + (y + z);
    reduce inv(x:t,y:t): x + y - y => x;
  }
  
Approximate Multiplicative Semi-Group With Unit.
------------------------------------------------

An approximate multiplicative semigroup is a set with a symmetric
binary multiplication operator and a unit. 


.. index:: FloatMultSemi1(class)
.. index:: muleq(proc)
.. index:: mul(fun)
.. index:: sqr(fun)
.. index:: cube(fun)
.. index:: one(fun)
.. code-block:: felix

  //[group.flx]
  //$ Multiplicative symmetric float-approximate semi group with unit symbol *.
  //$ Note: associativity is not assumed.
  class FloatMultSemi1[t] {
    inherit Eq[t];
    proc muleq(px:&t, y:t) { *= (px,y); }
    fun mul(x:t, y:t) => x * y;
    fun sqr(x:t) => x * x;
    fun cube(x:t) => x * x * x;
    virtual fun one: unit -> t;
    virtual fun * : t * t -> t;
    virtual proc *= (px:&t, y:t) { px <- *px * y; }
    reduce id (x:t): x*one() => x;
    reduce id (x:t): one()*x => x;
  }
  
Multiplicative Semi-Group With Unit.
------------------------------------

A multiplicative semigroup with unit is an approximate
multiplicative semigroup with unit and associativity
and satisfies the cancellation law.


.. index:: MultSemi1(class)
.. code-block:: felix

  //[group.flx]
  //$ Multiplicative semi group with unit.
  class MultSemi1[t] {
    inherit FloatMultSemi1[t];
    axiom assoc (x:t,y:t,z:t): (x * y) * z == x * (y * z);
    reduce cancel (x:t,y:t,z:t): x * z ==  y * z => x == y;
  }
  
Rings
=====


Approximate Unit Ring.
----------------------

An approximate ring is a set which has addition and
multiplication satisfying the rules for approximate
additive group and multiplicative semigroup respectively.


.. index:: FloatRing(class)
.. code-block:: felix

  //[ring.flx]
  //$ Float-approximate ring.
  class FloatRing[t] {
    inherit FloatAddgrp[t];
    inherit FloatMultSemi1[t];
  }
  
Ring
----

A ring is a type which is a both an additive group and
multiplicative semigroup with unit, and which in
addition satisfies the distributive law.


.. index:: Ring(class)
.. code-block:: felix

  //[ring.flx]
  //$ Ring.
  class Ring[t] {
    inherit Addgrp[t];
    inherit MultSemi1[t];
    axiom distrib (x:t,y:t,z:t): x * ( y + z) == x * y + x * z;
  }
Approximate Division Ring
-------------------------

An approximate division ring is an approximate ring with unit
with a division operator.


.. index:: FloatDring(class)
.. index:: div(fun)
.. index:: mod(fun)
.. index:: recip(fun)
.. index:: diveq(proc)
.. index:: modeq(proc)
.. code-block:: felix

  //[ring.flx]
  //$ Float-approximate division ring.
  class FloatDring[t] {
    inherit FloatRing[t];
    virtual fun / : t * t -> t; // pre t != 0
    fun \over (x:t,y:t) => x / y;
  
    virtual proc /= : &t * t;
    virtual fun % : t * t -> t;
    virtual proc %= : &t * t;
  
    fun div(x:t, y:t) => x / y;
    fun mod(x:t, y:t) => x % y;
    fun \bmod(x:t, y:t) => x % y;
    fun recip (x:t) => #one / x;
  
    proc diveq(px:&t, y:t) { /= (px,y); }
    proc modeq(px:&t, y:t) { %= (px,y); }
  }
  
Division Ring
-------------



.. index:: Dring(class)
.. code-block:: felix

  //[ring.flx]
  //$ Division ring.
  class Dring[t] {
    inherit Ring[t];
    inherit FloatDring[t];
  }
  
Integral.
=========


Bitwise operations
------------------



.. index:: Bits(class)
.. index:: bxor(fun)
.. index:: bor(fun)
.. index:: band(fun)
.. index:: bnot(fun)
.. code-block:: felix

  //[bits.flx]
  
  //$ Bitwise operators.
  class Bits[t] {
    virtual fun \^ : t * t -> t = "(?1)($1^$2)";
    virtual fun \| : t * t -> t = "$1|$2";
    virtual fun \& : t * t -> t = "$1&$2";
    virtual fun ~: t -> t = "(?1)(~$1)";
    virtual proc ^= : &t * t = "*$1^=$2;";
    virtual proc |= : &t * t = "*$1|=$2;";
    virtual proc &= : &t * t = "*$1&=$2;";
  
    fun bxor(x:t,y:t)=> x \^ y;
    fun bor(x:t,y:t)=> x \| y;
    fun band(x:t,y:t)=> x \& y;
    fun bnot(x:t)=> ~ x;
  
  }
Integer
-------



.. index:: Integer(class)
.. index:: shl(fun)
.. index:: shr(fun)
.. index:: Signed_integer(class)
.. index:: sgn(fun)
.. index:: abs(fun)
.. index:: Unsigned_integer(class)
.. code-block:: felix

  //[integer.flx]
  
  //$ Integers.
  class Integer[t] {
    inherit Tord[t];
    inherit Dring[t];
    inherit RandomSequence[t];
    virtual fun << : t * t -> t = "$1<<$2";
    virtual fun >> : t * t -> t = "$1>>$2";
  
    fun shl(x:t,y:t)=> x << y;
    fun shr(x:t,y:t)=> x >> y;
  }
  
  //$ Signed Integers.
  class Signed_integer[t] {
    inherit Integer[t];
    virtual fun sgn: t -> int;
    virtual fun abs: t -> t;
  }
  
  //$ Unsigned Integers.
  class Unsigned_integer[t] {
    inherit Integer[t];
    inherit Bits[t];
  }
  
  
  
Float kinds
===========


Trigonometric Functions.
------------------------

Trigonometric functions are shared by
real and complex numbers.


.. index:: Trig(class)
.. index:: sin(fun)
.. index:: cos(fun)
.. index:: tan(fun)
.. index:: sec(fun)
.. index:: csc(fun)
.. index:: cot(fun)
.. index:: asin(fun)
.. index:: acos(fun)
.. index:: atan(fun)
.. index:: asec(fun)
.. index:: acsc(fun)
.. index:: acot(fun)
.. index:: sinh(fun)
.. index:: cosh(fun)
.. index:: tanh(fun)
.. index:: sech(fun)
.. index:: csch(fun)
.. index:: coth(fun)
.. index:: asinh(fun)
.. index:: acosh(fun)
.. index:: atanh(fun)
.. index:: asech(fun)
.. index:: acsch(fun)
.. index:: acoth(fun)
.. index:: exp(fun)
.. index:: log(fun)
.. index:: ln(fun)
.. index:: pow(fun)
.. index:: pow(fun)
.. index:: Special(class)
.. index:: erf(fun)
.. index:: erfc(fun)
.. code-block:: felix

  //[trig.flx]
  
  //$ Float-approximate trigonometric functions.
  class Trig[t] {
    inherit FloatDring[t];
  
    // NOTE: most of the axioms here WILL FAIL because they require
    // exact equality, but they're only going to succeed with approximate
    // equality, whatever that means. This needs to be fixed!
  
    // circular
    // ref http://en.wikipedia.org/wiki/Circular_functions 
  
    // core trig
    virtual fun sin: t -> t;
    fun \sin (x:t)=> sin x;
  
    virtual fun cos: t -> t;
    fun \cos (x:t)=> cos x;
  
    virtual fun tan (x:t)=> sin x / cos x;
    fun \tan (x:t)=> tan x;
  
    // reciprocals
    virtual fun sec (x:t)=> recip (cos x);
    fun \sec (x:t)=> sec x;
  
    virtual fun csc (x:t)=> recip (sin x);
    fun \csc (x:t)=> csc x;
  
    virtual fun cot (x:t)=> recip (tan x);
    fun \cot (x:t)=> cot x;
  
    // inverses
    virtual fun asin: t -> t;
    fun \arcsin (x:t) => asin x;
   
    virtual fun acos: t -> t;
    fun \arccos (x:t) => acos x;
  
    virtual fun atan: t -> t;
    fun \arctan (x:t) => atan x;
  
    virtual fun asec (x:t) => acos ( recip x);
    virtual fun acsc (x:t) => asin ( recip x);
    virtual fun acot (x:t) => atan ( recip x);
  
    // hyperbolic
    // ref http://en.wikipedia.org/wiki/Hyperbolic_functions
    virtual fun sinh: t -> t;
    fun \sinh (x:t) => sinh x;
  
    virtual fun cosh: t -> t;
    fun \cosh (x:t) => cosh x;
  
    virtual fun tanh (x:t) => sinh x / cosh x;
    fun \tanh (x:t) => tanh x;
  
    // reciprocals
    virtual fun sech (x:t) => recip (cosh x);
    fun \sech (x:t) => sech x;
  
    virtual fun csch (x:t) => recip (sinh x);
    fun \csch (x:t) => csch x;
  
    virtual fun coth (x:t) => recip (tanh x); 
    fun \coth (x:t) => coth x;
  
    // inverses
    virtual fun asinh: t -> t;
  
    virtual fun acosh: t -> t;
  
    virtual fun atanh: t -> t;
  
    virtual fun asech (x:t) => acosh ( recip x);
    virtual fun acsch (x:t) => asinh ( recip x );
    virtual fun acoth (x:t) => atanh ( recip x );
  
    // exponential
    virtual fun exp: t -> t;
    fun \exp (x:t) => exp x;
  
    // log
    virtual fun log: t -> t;
    fun \log (x:t) => log x;
    fun ln (x:t) => log x;
    fun \ln (x:t) => log x;
  
    // power
    virtual fun pow: t * t -> t;
    virtual fun pow (a:t, b:int) : t => pow (a, C_hack::cast[t] b);
    fun ^ (x:t,y:t) => pow (x,y);
    fun ^ (x:t,y:int) => pow (x,y);
  
  
  }
  
  //$ Finance and Statistics.
  class Special[t] {
    virtual fun erf: t -> t;
    virtual fun erfc: t -> t;
  }
  
Approximate Reals.
------------------



.. index:: Real(class)
.. index:: embed(fun)
.. index:: log10(fun)
.. index:: abs(fun)
.. index:: sqrt(fun)
.. index:: ceil(fun)
.. index:: floor(fun)
.. index:: trunc(fun)
.. index:: atan2(fun)
.. code-block:: felix

  //[real.flx]
  //$ Float-approximate real numbers.
  class Real[t] {
    inherit Tord[t];
    inherit Trig[t];
    inherit Special[t];
    virtual fun embed: int -> t;
  
    virtual fun log10: t -> t;
    virtual fun abs: t -> t;
   
    virtual fun sqrt: t -> t;
    fun \sqrt (x:t) => sqrt x;
    virtual fun ceil: t -> t;
      // tex \lceil \rceil defined in grammar
  
    virtual fun floor: t -> t;
      // tex \lfloor \rfloor defined in grammar
  
    virtual fun trunc: t -> t;
  
    // this trig function is included here because it
    // is not available for complex numbers
    virtual fun atan2: t * t -> t;
  
  }
  
  
Complex numbers
---------------



.. index:: Complex(class)
.. index:: real(fun)
.. index:: imag(fun)
.. index:: abs(fun)
.. index:: arg(fun)
.. index:: sqrt(fun)
.. code-block:: felix

  //[complex.flx]
  //$ Float-approximate Complex.
  class Complex[t,r] {
    inherit Eq[t];
    inherit Special[t];
    inherit Trig[t];
    virtual fun real: t -> r;
    virtual fun imag: t -> r;
    virtual fun abs: t -> r;
    virtual fun arg: t -> r;
    virtual fun sqrt: t -> r;
  
    virtual fun + : r * t -> t;
    virtual fun + : t * r -> t;
    virtual fun - : r * t -> t;
    virtual fun - : t * r -> t;
    virtual fun * : t * r -> t;
    virtual fun * : r * t -> t;
    virtual fun / : t * r -> t;
    virtual fun / : r * t -> t;
  }
  
  
  
Summation and Product Quantifiers.
==================================

To be moved. Folds over streams.

.. index:: Quantifiers_add_mul(class)
.. code-block:: felix

  //[group.flx]
  open class Quantifiers_add_mul {
    fun \sum[T,C with FloatAddgrp[T], Streamable[C,T]] (a:C):T = 
    {
      var init = #zero[T];
      for x in a perform init = init + x;
      return init;
    }
  
    fun \prod[T,C with FloatMultSemi1[T], Streamable[C,T]] (a:C):T = 
    {
      var init = #one[T];
      for x in a perform init = init * x;
      return init;
    }
  
    fun \sum[T with FloatAddgrp[T]] (f:1->opt[T])  = 
    {
      var init = #zero[T];
      for x in f perform init = init + x;
      return init;
    }
  
    fun \prod[T with FloatMultSemi1[T]] (f:1->opt[T])  = 
    {
      var init = #one[T];
      for x in f perform init = init * x;
      return init;
    }
   
  }
  


Monad
=====


.. index:: Monad(class)
.. index:: ret(fun)
.. index:: bind(fun)
.. index:: join(fun)
.. code-block:: felix

  //[monad.flx]
  
  class Monad [M: TYPE->TYPE] {
    virtual fun ret[a]: a -> M a;
    virtual fun bind[a,b]: M a * (a -> M b) -> M b;
    fun join[a] (n: M (M a)): M a => bind (n , (fun (x:M a):M a=>x));
  }
  
  
  
