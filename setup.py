from setuptools import setup, find_packages

import imp

version = imp.load_source('clarsach.version', 'clarsach/version.py')

setup(
    name='clarsach',
    version=version.version,
    description='Clarsach',
    author='Daniela Huppenkothen',
    author_email='daniela.huppenkothen@nyu.edu',
    url='http://github.com/dhuppenkothen/clarsach',
    download_url='http://github.com/dhuppenkothen/clarsach/releases',
    packages=find_packages(),
    long_description="""Clarsach""",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering :: Astronomy"
    ],
    license='GPL',
    install_requires=[
        'numpy>=1.10',
        'astropy>=1.0.0',
    ],
    extras_require={
        'docs': ['numpydoc']
    }
)

