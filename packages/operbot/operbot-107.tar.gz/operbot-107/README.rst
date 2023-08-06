README
######


**NAME**


``OPERBOT`` - write your own commands


**SYNOPSIS**


| ``operbot [-c] [-i] [-r]``
| ``operbot <cmd> [key=value] [key==value]``
|


**DESCRIPTION**


``OPERBOT`` is a solid, non hackable bot, intended to be programmable in a
static, only code, no popen, fixed imports and no reading modules from a
directory, to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are also avoided, direct
imports in the code is what is used.

``OPERBOT`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object.

``OPERBOT`` has some functionality, mostly feeding RSS feeds into a irc
channel. It can do some logging of txt and take note of things todo.



**INSTALL**

|
| ``pip3 install operbot --upgrade --force-reinstall``
|

**CONFIGURATION**

|
| configuration is done by calling the ``cfg`` command of ``operbot``
| 

**irc**


| ``operbot cfg server=<server> channel=<channel> nick=<nick>``
|
| (*) default channel/server is #operbot on localhost
|

**sasl**


| ``operbot pwd <nickservnick> <nickservpass>``
| ``operbot cfg password=<outputfrompwd>``
|

**users**


| ``operbot cfg users=True``
| ``operbot met <userhost>``
|

**rss**


| ``operbot rss <url>``
|


**RUNNING**


this part shows how to run ``operbot``.

**cli**

without any arguments ``operbot`` doesn't respond, add arguments to have
``operbot`` execute a command:


| ``$ operbot``
| ``$``
|

the ``cmd`` command shows you a list of available commands:


| ``$ operbot cmd``
| ``cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,log,met,mre,nme,pwd,rem,rss,tdo,thr,ver``
|

**console**

use the -c option to start the bot as a console.


| ``$ operbot -c``
| ``OPERBOT started at Fri Sep 16 02:11:23 2022``
| ``> cfg``
| ``server=localhost port=6667 channel=#operbot nick=operbot cc=!``
| ``> thr``
| ``Console.loop(8s) IRC.keep(8s) IRC.loop(8s) IRC.output(8s) thr(8s) Fetcher.run/4m59s``
|

**COMMANDS**


here is a short description of the commands.


| ``cfg`` - show the irc configuration, also edits the config
| ``cmd`` - show all commands
| ``dlt`` - remove a user
| ``dne`` - flag todo as done
| ``dpl`` - set display items for a rss feed
| ``flt`` - show a list of bot registered to the bus
| ``fnd`` - allow you to display objects on the datastore, read-only json files on disk 
| ``ftc`` - run a rss feed fetching batch
| ``log`` - log some text
| ``met`` - add a users with there irc userhost
| ``mre`` - displays cached output, channel wise.
| ``nme`` - set name of a rss feed
| ``pwd`` - combine a nickserv name/password into a sasl password
| ``rem`` - remove a rss feed by matching is to its url
| ``rss`` - add a feed to fetch, fetcher runs every 5 minutes
| ``thr`` - show the running threads
| ``tdo`` - adds a todo item, no options returns list of todo's
| ``upt`` - show uptime
| ``ver`` - show version
|


**PROGRAMMING**


The ``operbot`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> from operbot import Object
>>> o = Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from operbot import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> from operbot import Object, save
 >>> o = Object()
 >>> save(o)
 operbot.object.Object/89efa5fd7ad9497b96fdcb5f01477320/2022-11-21/17:20:12.221192

**SYSTEMD**

to run the bot after reboot, install the service file and start the service
by enabling it with ``--now``::


 $ ``sudo cp /usr/local/share/operbot/operbot.service /etc/systemd/system``
 $ ``sudo systemctl enable operbot --now``

 (*) default channel/server is #operbot on localhost

 use ``operbotctl`` instead of the use ``operbot`` program

 $ ``sudo operbotctl cfg server=<server> channel=<channel> nick=<nick>``
 $ ``sudo operbotctl pwd <nickservnick> <nickservpass>``
 $ ``sudo operbotctl cfg password=<outputfrompwd>``
 $ ``sudo operbotctl cfg users=True``
 $ ``sudo operbotctl met <userhost>``
 $ ``sudo operbotctl rss <url>``


**AUTHOR**


Bart Thate - operbot100@gmail.com


**COPYRIGHT**


``operbot`` is placed in the Public Domain. No Copyright, No License.
