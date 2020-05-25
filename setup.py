import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="flashpoint-indexer",
    version="1.0.0",
    description="Creates/Updates an Index of files with hashes in a directory",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FlashpointProject/FlashpointIndexer",
    author="Colin Berry",
    author_email="colin.berry.work@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "fpindexer=fpindexer.__main__:main",
        ]
    },
)
