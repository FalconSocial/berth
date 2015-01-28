"""setup.py for the berth package."""

from setuptools import setup

setup(
    name='berth',
    version='1.0.0',
    description='Utility to generate package files using Docker containers',
    author='Falcon Social',
    url='https://github.com/FalconSocial/berth',
    license='MIT',
    packages=['berth'],
    install_requires=[
        'click >= 3, < 4',
        'docker-py >= 0.7, < 0.8',
        'PyYAML >= 3, < 4',
    ],
    entry_points={
        'console_scripts': [
            'berth = berth.cli:main',
        ]
    }
)
