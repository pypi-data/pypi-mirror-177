from setuptools import *

setup(
    name='CLUIE',
    version='0.1.7',
    description='Python Command-Line User-Interface Engine',
    url='https://github.com/mategol/CLUIE-python',
    author='Mateusz Golembowski',
    author_email='mateusz@golembowski.pl',
    license='MIT',
    packages=['CLUIE'],
    install_requires=['cursor',
                      ],

    classifiers=[
        'License :: OSI Approved :: MIT License',      
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)