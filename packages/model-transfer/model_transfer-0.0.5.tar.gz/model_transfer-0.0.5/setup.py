# coding=utf8
__author__ = 'liming'

from setuptools import setup

setup(name='model_transfer',
      version='0.0.5',
      description='Convert Model Lang to All Kinds of model classes',
      url='https://github.com/ipconfiger',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='GPL-3.',
      packages=['model_transfer'],
      install_requires=['jinja2', 'click'],
      entry_points={
          'console_scripts': ['mtf=model_transfer.main:main'],
      },
      zip_safe=False)
