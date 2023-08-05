# import os
from setuptools import find_packages, setup

# BASE_DIR = os.path.dirname(__file__)

# with open(os.path.join(BASE_DIR, 'requirements.txt'), 'r') as fp:
#     REQS = [pkg.strip() for pkg in fp]

setup(
    name='kyle-degennaro-sdk',
    version='1.0.1',
    license='MIT',
    author='github.com/KED',
    url='https://github.com/KED/kyle_degennaro-SDK',
    packages=find_packages(),
    install_requires=['pydantic==1.10.2', 'requests==2.28.1'],
    python_requires='>=3.9',
)