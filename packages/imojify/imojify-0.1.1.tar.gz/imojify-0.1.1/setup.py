from setuptools import find_packages, setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='imojify',
    packages=find_packages(include=['imojify']),
    include_package_data=True,
    version='0.1.1',
    url="https://github.com/abdulrahmankhayal/imojify",
    description='a python library that imagify emoji-unicode',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Abdul-Rahman Khayyal',
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    install_requires=['emoji','numpy','Pillow'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['Images/*']
    }
)
