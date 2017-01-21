from setuptools import setup, find_packages

long_description = 'Imports the full socHACKi Library'

setup(
    name='socHACKi',
    version='0.0.0',
    license='BSD',
    description='Imports the full socHACKi Library',
    long_description=long_description,
    author='John Sochacki',
    author_email='johnsochacki@hotmail.com',
    url='https://github.com/jsochacki/',
    packages = find_packages(exclude=['*test*']),
    install_requires=['pandas>=0.18.1','tabulate'],
    keywords = ['Type Conversion', 'Pandas', 'Visio'],
)
