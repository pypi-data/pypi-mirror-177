import os
import setuptools
from setuptools import setup


def get_readme():
    with open("README.md", "r") as f:
        return f.read()


def read_requirements_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f]



setup(
    name='rosamplepackage',
    version='0.0.2',
    description='The smallest python package module to test.',
    url='http://github.com/rosikand/rosamplepackage',
    author='Rohan Sikand',
    author_email='rohansikand2024@gmail.com',
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    # license='MIT',
    packages=setuptools.find_packages(),
    install_requires=read_requirements_file('requirements.txt')
)
