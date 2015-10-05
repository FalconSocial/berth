"""setup.py for the berth package."""

from setuptools import setup

LONG_DESCRIPTION = '''Berth is a tool to help you automate the building of packages for an array of operating system and package systems, while not putting a big load on the local dependencies where you build the packages.

It does this by using a Docker container of your choice to build your project inside, and then use another container with the `FPM <https://github.com/jordansissel/fpm>`_ package creator inside to package up the project.

Read more on `GitHub <https://github.com/FalconSocial/berth>`_.'''

with open('CHANGELOG.md') as changelog:
    LONG_DESCRIPTION += '\n\n'
    LONG_DESCRIPTION += changelog.read()

setup(
    name='berth',
    version='1.3.4',
    description='Utility to generate package files using Docker containers',
    long_description=LONG_DESCRIPTION,
    author='Falcon Social',
    url='https://github.com/FalconSocial/berth',
    license='MIT',
    packages=['berth'],
    install_requires=[
        'click >= 5, < 6',
        'docker-py >= 1.3.1, < 2',
        'PyYAML >= 3, < 4',
    ],
    entry_points={
        'console_scripts': [
            'berth = berth.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ],
)
