===========
Description
===========

Run Nautilus scripts within Thunar file manager. Tuna-wrap wraps
Nautilus filemanager scripts to run these from Thunars custom actions.

**License**

    MIT License

**Notes**

    * Only tested on ubuntu with nautilus scripts written in python
    * Only tested with python3

========
Features
========

    * share you scripts between Thunar, Nautilus and Nemo
    * very easy use

============
Installation
============

**Installation / Deinstallation**

    *with pip*
        
        ::
        
            pip3 install tuna-wrap
    
            pip3 uninstall tuna-wrap


    *or setup.py*

        1. Unpack your package.
        2. Open a terminal and change to the folder which contains the setup.py and type

        ::

            python setup.py install
   
=====
Setup
=====
    
    * Edit your Thunar custom actions in following scheme:
      tuna-wrap "YOUR NAUTILUS SCRIPT NAME" "%d" "%N"
    * Make sure your scripts are in one of these places:
    
          ~/.local/share/nautilus/scripts/
          ~/.scripts/
          ~/.local/share/nemo/scripts/
          
    * Do´t forget to make your scripts executable
      
=====
Usage
=====

    * Use it as your other custom actions
    * get this readme with: tuna-wrap --help
    
=====
Hints
=====

    * The logfile is stored in you home directory: ~/.tuna-wrap.log
    * For a more verbose tuna-wrap output add "DEBUG" as last argument
