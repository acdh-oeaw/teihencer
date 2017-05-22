from setuptools import setup, find_packages
from codecs import open
from os import path

# python setup.py bdist_wheel

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='tei',
    version='0.5.0',
    description='A package to process and enhance TEI-Documents',
    long_description=long_description,
    url="https://redmine.acdh.oeaw.ac.at/issues/8711",
    author="Peter Andorfer",
    author_email="peter.andorfer@oeaw.ac.at",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: TEI',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='TEI, XML',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['lxml'],
)
