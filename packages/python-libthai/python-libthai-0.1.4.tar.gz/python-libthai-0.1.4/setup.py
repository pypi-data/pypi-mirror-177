#-*- coding: UTF-8 -*-
from setuptools import setup,find_packages,Command, Extension
import os

setup(
    name="python-libthai",
    version="0.1.4",
    packages=['pythai'],

    ext_modules=[ 
        Extension("libthai", 
                  ["pythai/libthai.c"],
                  libraries=['thai'])],

    # Required repositories
    install_requires=[
        'nose',
        'six',
        'future>=0.16.0'
    ],
    package_data = {
        'pythai': ['LICENSE.txt', 'README.md']
    },

    # metadata for upload to PyPI
    author = "Teerasit Angkhaprsertkul",
    author_email = "teerasit.ang@gmail.com",
    description = "Python - libthai binding library.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    license = "GNU",
    keywords = "thai language linguistics segmentation",
    url = "https://github.com/teerasit-ang",
    test_suite='pythai.tests',

    # could also include long_description, download_url, classifiers, etc.
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ]

)
