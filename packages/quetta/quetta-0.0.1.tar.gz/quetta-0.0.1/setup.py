from setuptools import setup, find_packages

setup(name='quetta',
      version='0.0.1',
      author='mono',
      author_email='immonomono@gmail.com',
      description='tools for MLOps',
      packages=find_packages(exclude=['']),
      long_description=open('README.md').read(),
      install_requires=[''],
)
