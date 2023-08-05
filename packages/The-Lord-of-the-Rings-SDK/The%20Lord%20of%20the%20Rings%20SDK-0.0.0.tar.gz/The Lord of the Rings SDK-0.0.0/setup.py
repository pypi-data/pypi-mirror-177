import os
from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'requirements.txt'), 'r') as fp:
    REQS = [pkg.strip() for pkg in fp]

setup(
    name='The Lord of the Rings SDK',
    license='MIT',
    author='github.com/KED/kyle_degennaro-sdk',
    packages=find_packages(),
    install_requires=REQS,
)