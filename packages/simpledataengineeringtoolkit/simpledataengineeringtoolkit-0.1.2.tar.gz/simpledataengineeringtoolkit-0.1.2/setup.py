from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="simpledataengineeringtoolkit",
    version="0.1.2",
    description="Data Engineers Toolkit library",
    long_description='Data Engineers Toolkit library',
    long_description_content_type='text/markdown',
    url="https://simpledataengineeringtoolkit.readthedocs.io/",
    author="Ahmad Karrabi",
    author_email="ahmad@karrabi.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["simpledataengineeringtoolkit"],
    include_package_data=True,
    install_requires=["pandas"]
)