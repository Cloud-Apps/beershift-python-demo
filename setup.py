from setuptools import setup

setup(name='OpenShift BeerShift Server',
      version='1.0',
      description='BeerShift Server in Python using MongoDB',
      author='Mark Atwood',
      author_email='matwood@redhat.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['bottle','pymongo'],
     )
