from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

setup(name='dexpresso', version='0.3.2', packages=find_packages())
