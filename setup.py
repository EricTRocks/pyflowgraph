# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='pyflowgraph',
      version='0.1',
      description='An interactive data flow graph editor',
      url='https://github.com/HordeSoftware-co/pyflowgraph',
      author='',
      author_email='',
      license='MIT',
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
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
      ],
      packages=['pyflowgraph'],
      install_requires=['qtpy', 'six', 'future'],
      zip_safe=False)

