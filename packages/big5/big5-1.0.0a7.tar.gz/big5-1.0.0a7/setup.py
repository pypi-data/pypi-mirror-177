import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 9)

if sys.version_info[:2] < MIN_PYTHON_VERSION:
    raise RuntimeError('Python version required = {}.{}'.format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import big5

REQUIRED_PACKAGES = [

]

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Natural Language :: Russian
Natural Language :: English
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Artificial Intelligence
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
"""

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = big5.__name__,
        packages = find_packages(),
        license = big5.__license__,
        version = big5.__release__,
        author = big5.__author__en__,
        author_email = big5.__email__,
        maintainer = big5.__maintainer__en__,
        maintainer_email = big5.__maintainer_email__,
        url = big5.__uri__,
        description = big5.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['big5', 'MachineLearning', 'Statistics', 'ComputerVision', 'ArtificialIntelligence',
                    'Preprocessing'],
        include_package_data = True,
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.9, <4',
        entry_points = {
            'console_scripts': [],
        },
        project_urls = {
            'Bug Reports': 'https://github.com/DmitryRyumin/big5/issues',
            'Documentation': 'https://big5.readthedocs.io',
            'Source Code': 'https://github.com/DmitryRyumin/big5/tree/main/big5',
            'Download': 'https://github.com/DmitryRyumin/big5/tags',
        },
    )
