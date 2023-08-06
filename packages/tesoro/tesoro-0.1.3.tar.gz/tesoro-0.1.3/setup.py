from setuptools import setup, find_packages


setup(
    name = 'tesoro',
    version = '0.1.3',
    packages = find_packages(exclude=['tests']),
    install_requires = ['requests>=2.6', 'responses', 'nose'],
    url = 'https://github.com/octoenergy/tesoro-lib',
)
