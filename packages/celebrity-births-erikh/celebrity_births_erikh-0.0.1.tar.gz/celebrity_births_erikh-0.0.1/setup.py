from setuptools import setup
from setuptools import find_packages

setup(
    name='celebrity_births_erikh', ## This will be the name your package will be published with
    version='0.0.1', 
    description='Mock package that allows you to find celebrity by date of birth',
    url='https://github.com/eharaldson/project-structure-mini-challenge-1.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Erik Haraldson', # Your name
    license='Oxford',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['requests', 'beautifulsoup4'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)