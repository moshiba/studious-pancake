# studious-pancake

[![Build Status](https://travis-ci.com/HsuanTingLu/studious-pancake.svg?token=tDHixgpdZAhsXN1fMdDk&branch=master)](https://travis-ci.com/HsuanTingLu/studious-pancake)

Mysterious structure bond pruning routine wrapper,  
with parallel task dispatching ability

needs installation before run

## Prerequisites
- python 3.7 or higher (due to the use of f-strings)
- [LAMMPS](http://lammps.sandia.gov/)
  - needs the normal python bonding of LAMMPS instead of the PyLAMMPS interface

## Install

run `pip3 install -e .` **AT THE ROOT DIRECTORY**


## Usage

Place a datafile named `"data.file"` at the root directory,  
(the original version of it named `"data.file.ORIG"` is in `./tests/data/`)

then execute the main script by running `python3 main.py` **AT THE ROOT DIRECTORY**

## Developers' Nook

### Prerequisites

required packages are listed in `requirements.txt`
(running `pip3 install requirements.txt` would do)

### Testing

run `pytest` **AT THE ROOT DIRECTORY**
