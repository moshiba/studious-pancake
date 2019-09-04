"""

    setuptools script
    Copyright (C) 2019 Hsuan-Ting Lu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gonko",
    version="1.2.0",
    author="HsuanTingLu",
    author_email="hsuan.ting.lu.ee05@g2.nctu.edu.tw",
    description=
    "Mysterious structure bond pruning routine wrapper with parallel task dispatching ability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HsuanTingLu/studious-pancake",
    packages=setuptools.find_packages(),
    install_requires=["tqdm", "psutil"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 1 - Planning", "Environment :: Console",
        "Framework :: Pytest", "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: English", "Operating System :: POSIX",
        "Topic :: Scientific/Engineering :: Physics"
    ],
)
