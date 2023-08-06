README
######

NAME
====

**oplib** - object programming library

INSTALL
=======

sudo pip3 install oplib --upgrade --force-reinstall


DESCRIPTION
===========


The ``oplib`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> import opl
>>> o = opl.Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> import opl
>>> o = opl.Object()
>>> o.key = "value"
>>> p = opl.save(o)
>>> oo = opl.Object()
>>> opl.load(oo, p)
>>> oo.key
>>> 'value'

great for giving objects peristence by having their state stored in files.

>>> import opl
>>> opl.Wd.workdir = ".test"
>>> o = op.Object()
>>> opl.save(o)
'opl.obj.Object/2021-08-31/15:31:05.717063'


AUTHOR
======

Bart Thate - bthate67@gmail.com


COPYRIGHT
=========

**OPLIB** is placed in the Public Domain, no Copyright, no LICENSE.
