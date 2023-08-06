#!/usr/bin/env python

from setuptools import setup

setup(
    name='helloworld_123_test',
    version='0.0.1',
    description='Say hello',
    py_modules=["helloworld_123_test"],
    package_dir={'': 'src'},
    author='Di Wang',
    author_email='di-wang@uiowa.edu',
    url='https://github.com/daisydiwang/helloworld_123_test',
    keywords=['3D brain image', 'statistics', 'hierarchical structure'],
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy', 
        'pandas',
    ]
)


# author='Di Wang',
# author_email='di-wang@uiowa.edu',
# packages=find_packages(),
# packages=["baz", "bar", "foo"],
# install_requires=['numpy', 'pandas'],
# packages=['helloworld'],




# from setuptools import setup
# from os import path
# DIR = path.dirname(path.abspath(__file__))

# with open(path.join(DIR, 'README.md')) as f:
#     README = f.read()


# VERSION='0.0.1'
# DESCRIPTION='Calculate 3D brain region signal statistics'

# setup(
#     name='brain_region_signal_statistics_calculalor',
#     version=VERSION,
#     author='Di Wang',
#     author_email='di-wang@uiowa.edu',
#     description=DESCRIPTION,
#     long_description_content_type='text/markdown',
#     long_description=README,
#     install_requires=['numpy', 'pandas'],
#     packages=['brain_region_signal_statistics_calculalor'],
#     url='https://github.com/daisydiwang/brain_region_signal_statistics_calculalor',

#     keywords=['3D brain image', 'statistics', 'hierarchical structure'],
#     python_requires='>=3'
# )

# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
# install_requires=INSTALL_PACKAGES,