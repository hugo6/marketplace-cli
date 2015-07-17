UShareSoft UForge Marketplace CLI
=====

A command-line tool to interact with the UForge Marketplace webservice. 

Installation
============
marketplacecli is based on python, consequently it supports all major operating systems.  The easiest way to install marketplacecli is using `pip`.

```
$ pip install marketplacecli 
```

Installing From Source
======================
marketplacecli has a dependency to uforge-marketplace_python_sdk. First, you need to install it:

```
$ pip install uforge-marketplace_python_sdk
```

or download sources from pypi: https://pypi.python.org/pypi/uforge-marketplace_python_sdk

Go to the source directory where the `setup.py` file is located.

To compile and install, run (as sudo):

```
$ sudo python setup.py build install
```

Now clone the marketplacecli git repository to get all the source files.
Next go to the source directory where the `setup.py` file is located.
To compile and install, run (as sudo):

```
$ sudo python setup.py build install
```

This will automatically create the marketplacecli executable and install it properly on your system.

To check that this was successful, run:

```
$ marketplacecli —v 
```

Upgrading
=========
If you have already installed marketplacecli, and you with to upgrade to the latest version, use:
```
$ pip install —upgrade marketplacecli
```

License
=======
marketplacecli is licensed under the Apache 2.0 license. For more information, please refer to LICENSE file.
