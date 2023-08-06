from setuptools import find_packages, setup

setup(
  name='erp5_coverage_plugin',
  version='0.0.1',
  packages=find_packages(),
  install_requires=['coverage'],
  extras_require={'test': ['pytest', 'Products.PythonScripts']},
)
