Clàrsach: Lightweight response matrix calculations in Python
============================================================

+------------------+-------------------------+---------------------------+
| Master           | |Build Status Master|   | |Coverage Status Master|  |
+------------------+-------------------------+---------------------------+


The analysis of X-ray spectra often depends on the correct 
usage of instrument response files. However, these calculations 
are exclusively implemented in one of the three X-ray packages, 
all of which come with a lot of overhead. 

Here, we attempt to separate out and simplify the response calculation in 
sherpa for ease of use with any other (user-written) code. 

Installing Clàrsach
-------------------

Clàrsach currently lives exclusively on GitHub (we might upload it to 
pip once it's a little better developed). 

Please note: Clàrsach comes with a suite of tests and test data sets that 
checks whether the code words for a range of different X-ray telescopes. We 
strongly urge you to download the test data and run those tests! We provide
instructions for both with and without the test data.

Installing with the Test Data
-----------------------------
 
Because the test data files are large, we do not keep them in the repository, but 
in a system called the Git Large File System (``git lfs``). 
This is an extension for git maintained by GitHub, and can be downloaded on the
`git lfs website <https://git-lfs.github.com>`_ or your favourite package manager.

In order to download the repository with the test data, you then move to the directory 
where you wish the code to live and type:::

	git lfs clone git@github.com:dhuppenkothen/clarsach.git

	git lfs pull origin master

Then move into the ``clarsach`` directory. You can install the package by running::

	python setup.py install

Depending on your python installation and set up, this may require administrator privileges.
Finally, run the tests using ``py.test`` (you may need to install that, too):::

	py.test

Hopefully, this should run without throwing errors. If it does, please contact us through 
the `issues <https://github.com/dhuppenkothen/clarsach/issues>`_.  

Installing without the Test Data
--------------------------------

You can use standard git for cloning the repository, but be aware that the test data 
will not be downloaded. 

In order to download the repository, do the following:::

	git clone git@github.com:dhuppenkothen/clarsach.git

In order to install it, you move into the ``clarsach`` directory this will 
create and do the following:::

	python setup.py install

This should install Clàrsach on your system. Please note that your permissions 
might require you to use ``sudo`` in order to install the package.

Copyright
---------
All content copyright © 2017 the authors. The code is distributed under a GPL licence.


Contact
-------
Pull requests are welcome! If you are interested in the further development of
this project, if you find bugs, or have suggestions or comments, please feel free to contact us through 
the `issues <https://github.com/dhuppenkothen/clarsach/issues>`_.



.. |Build Status Master| image:: https://travis-ci.org/dhuppenkothen/clarsach.svg?branch=master

Example data for testing the functionality of Clarsach can be obtained via the following public link:
https://uwmadison.box.com/s/im9ke8cdjta8nc2npgvg70zz917kvvfi

Uploaded by lia@astro.wisc.edu

