from setuptools import find_packages, setup

setup(
    where='.',
    packages = find_packages(
        exclude=['tests*', 'tests']
        )
)