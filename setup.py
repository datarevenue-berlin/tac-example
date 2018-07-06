from setuptools import setup, find_packages

setup(
    name='tac',
    version='0.1',
    install_requires=[
      'luigi',
      'docker',
      'click',
    ],
    packages=find_packages(),
)


