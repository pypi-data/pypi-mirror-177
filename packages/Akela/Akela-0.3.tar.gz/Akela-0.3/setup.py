from setuptools import setup, find_packages
from os.path import join, dirname
import re

s = open("akela/__init__.py").read().split('\n')[0]
__version__ = re.search('\"[0-9\.]+\"$', s).group()[1:-1]

setup(
   name='Akela',
   version=__version__,
   author='sherekhan at pypi.org',
   author_email='sherekhan@jungle.tes',
   packages=find_packages(),
   license='GNU GPL3+',
   description='Offline browser converting HTML to Markdown',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "requests>=2.22.0",
       "markdownify>=0.11.2",
       "libzim>=2.0.0"
   ],
   classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Natural Language :: Russian"
    ],
   entry_points={
        'console_scripts':
            ['Akela = akela.geturi:start',
            'Akela-find = akela.find:start',
            'Akela-sync = akela.sync:sync']
        }
)
