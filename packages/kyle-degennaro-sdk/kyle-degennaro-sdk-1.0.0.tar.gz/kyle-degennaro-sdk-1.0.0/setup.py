import os
from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'requirements.txt'), 'r') as fp:
    REQS = [pkg.strip() for pkg in fp]

setup(
    name='kyle-degennaro-sdk',
    version='1.0.0',
    license='MIT',
    author='github.com/KED',
    url='https://github.com/KED/kyle_degennaro-SDK',
    packages=find_packages(),
    install_requires=REQS,
    python_requires='>=3.9',
)