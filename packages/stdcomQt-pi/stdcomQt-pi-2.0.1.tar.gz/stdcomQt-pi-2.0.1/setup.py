import setuptools
from setuptools import setup


setup(
    name='stdcomQt-pi',
    version="2.0.01",
    license_files = ('LICENSE.txt',),
    packages=['stdcomQtPiPlate', 'stdcomLabjack' ],
    package_dir={'': 'src'},
    url='http://www.vremsoft.com',
    license='LICENSE.txt',
    author='ed',
    author_email='srini_durand@yahoo.com',
    description='Stec Railway Version StandAlone Subscribers Labjack and piplates'      ,
    classifiers = [
                  "Programming Language :: Python :: 3",
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Programming Language :: Python :: 3.9",
                  "Programming Language :: Python :: 3.10",
                  "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                  "Operating System :: OS Independent",
              ],



    requires = ["setuptools", "wheel","PyQt5"],
    install_requires =["PyQt5"],
    include_package_data=True

)
