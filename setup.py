from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='openlobby',
    version='0.1.0',
    url='https://github.com/openlobby/openlobby-server',

    author='Jan Bednarik',
    author_email='jan.bednarik@gmail.com',

    description='Open Lobby Server',
    long_description=long_description,

    packages=find_packages(exclude=['tests']),

    # TODO
    # install_requires=[],
    # extras_require={
    #     'dev': [],
    #     'test': [],
    # },

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
