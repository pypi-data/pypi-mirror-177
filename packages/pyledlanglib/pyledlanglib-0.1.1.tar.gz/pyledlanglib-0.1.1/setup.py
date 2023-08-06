from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

setup(
    name='pyledlanglib',
    version='0.1.1',    
    description='PyLEdLang compiler on top of Python3',
    long_description = "",
    url='https://github.com/alex5250/PyLEDLang-Compiler',
    author='Alex Zaslavskis',
    author_email='sahsariga111@gmail.com',
    license='BSD 2-clause',
    packages=['pyledlanglib'],
    install_requires=[''],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.11',
    ],
)
