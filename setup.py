from setuptools import setup, find_packages
from codecs import open
from os import path
import os
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def find_all(folder):
    for (path, directories, filenames) in os.walk(folder):
        for filename in filenames:
            yield os.path.join('..', path, filename)

setup(
    name='avell-unofficial-control-center',
    version='1.0.2',
    description='A Project to provide a driver and interface to control keyboard rgb led of ITE 8291 like Avell laptops',  # Required
    entry_points={'console_scripts': [
        'aucc = aucc.main:main']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rodgomesc/avell-unofficial-control-center',  # Optional
    author='Rodrigo Gomes da Cunha',
    author_email='rodgomesc@gmail.com',
    packages=find_packages(),
    package_data={'': [file for file in find_all('aucc')]},
    include_package_data=True,
    install_requires=[
	'pyusb',
	'elevate'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/rodgomesc/avell-unofficial-control-center/issues',
        'Funding': 'https://www.buymeacoffee.com/KCZRP52U7',
        'Source': 'https://github.com/rodgomesc/avell-unofficial-control-center',
    },
)
