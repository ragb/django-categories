
from distutils.core import setup
from categories import version as package_version

""" django-categories instalation script """
setup(
    name = 'categories',
    description = 'generic categories application for django',
    author = 'Rui Batista',
    author_email = 'ruiandrebatista@gmail.com',
    version = package_version[0] + "." + package_version[1] + package_version[2],
    packages = ['categories'],
    )
