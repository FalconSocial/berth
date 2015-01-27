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
        'click',
        'docker-py',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'berth = berth.cli:main',
        ]
    }
)
