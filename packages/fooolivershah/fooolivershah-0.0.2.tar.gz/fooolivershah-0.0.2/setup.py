from setuptools import find_packages
from numpy.distutils.core import setup, Extension
import site
import os
# from setuptools import setup, Extension

# site.ENABLE_USER_SITE = os.geteuid() != 0

PACKAGE_NAME = 'fooolivershah'

# Generate object files for static linking:
# TODO: Execute command to compile .f90 files

# Specify the object files for static linking
# Must be pre-compiled at this point
extra_object = '{}/bar/three.o'.format(PACKAGE_NAME)


ext1 = Extension(name='{}.one'.format(PACKAGE_NAME),
                 sources=['{}/one.f90'.format(PACKAGE_NAME)],
                f2py_options=['--quiet'],
                )

ext2 = Extension(name='{}.bar.two'.format(PACKAGE_NAME),
                 sources=['{}/bar/two.f90'.format(PACKAGE_NAME)],
                 extra_objects=[extra_object],
                 #libraries=['three'], # --> does not work!
                f2py_options=['--quiet'],
                )

ext3 = Extension(name='{}.main'.format(PACKAGE_NAME),
                 sources=['{}/main.py'.format(PACKAGE_NAME)],
                f2py_options=['--quiet'],
                )

setup(
        name=PACKAGE_NAME,
      version="0.0.2",
      #package_dir={"": "foo"}, # --> does not include .py files!
      packages=find_packages(),
      ext_modules=[ext1, ext2, ext3],
      # py_modules = ['main', 'bar.myclass'], # --> does not work!
      optional=os.environ.get('CIBUILDWHEEL', '0') != '1',
      )
      


# from numpy.distutils.core import setup
# from numpy.distutils.misc_util import Configuration

# config = Configuration('foo')
# config.packages=['foo','foo.bar']
# config.add_extension('bar.two',
#     sources=['foo/bar/two.f90'],
#     libraries=['two'])

# config.add_library('three',
#     sources=['foo/bar/three.f90'])   

# setup(**config.todict())