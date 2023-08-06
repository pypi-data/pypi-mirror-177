from setuptools import setup, find_packages

setup(
    name='arhitecture',
    version='1.6',
    packages=find_packages(),
    entry_points = {
      'console_scripts':
            ['startproject = arhitecture.Start:startapp']
    },
    author_email='sbolid-test@yandex.ru'
)
