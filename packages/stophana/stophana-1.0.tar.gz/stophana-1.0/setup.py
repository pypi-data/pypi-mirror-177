import setuptools
from setuptools import setup


setup(
    name='stophana',
    version='1.0',
    author='jean',
    author_email='6159984@gmail.com',
    description='this is a test of packaging and publishing',
    long_description=open('README.md', 'r').read(),
    url='https://sdfgsad.com',
    package_data={
        'pythonProject_pkg': ['*']},
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)