# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = """An interactive data flow graph editor."""

setup(name='pyflowgraph',
      version='0.0.3',
      description='An interactive data flow graph editor',
      long_description=long_description,
      url='https://github.com/EricTRocks/pyflowgraph',
      author='Eric Thivierge',
      author_email='ethivierge@gmail.com',
      license='BSD 3-clause "New" or "Revised" License',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
      ],
      keywords='data flow graph',
      packages=find_packages(exclude=['tests']),
      install_requires=['PySide>=1.2.2,<1.2.4','qtpy','six','future'],
      zip_safe=False)

