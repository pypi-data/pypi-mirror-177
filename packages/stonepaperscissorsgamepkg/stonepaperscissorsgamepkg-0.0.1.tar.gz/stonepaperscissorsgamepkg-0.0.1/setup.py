from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Rock Paper Scissors - a basic program to play rock,paper,scissors with PC"
with open("README.md",'r') as fp:
    LONG_DESCRIPTION=fp.read()

# setting up
setup(
    name="stonepaperscissorsgamepkg",
    version=VERSION,
    author="Aswin Venkat",
    author_email="<aswinvenk8@gmail.com>",
    url="https://github.com/aswinvenk/stonepaperscissorsgamepkg",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_dir = {"": "src"},
    packages=find_packages(where="src"),
    keywords=['python','game','rock paper scissors', 'stone paper scissors'],
    license="LICENSE.txt",
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Rock Paper Scissors - a basic program to play rock,paper,scissors with PC"
with open("README.md",'r') as fp:
    LONG_DESCRIPTION=fp.read()

# setting up
setup(
    name="stonepaperscissorsgamepkg",
    version=VERSION,
    author="Aswin Venkat",
    author_email="<aswinvenk8@gmail.com>",
    url="https://github.com/aswinvenk/stonepaperscissorsgamepkg",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_dir = {"": "src"},
    packages=find_packages(where="src"),
    keywords=['python','game','rock paper scissors', 'stone paper scissors'],
    license="LICENSE.txt",
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
