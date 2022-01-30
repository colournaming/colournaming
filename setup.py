import os.path
from setuptools import find_packages, setup

NAME = 'colournaming'
version = open(os.path.join(NAME, 'VERSION')).read().strip()


setup(
    name=NAME,
    version=version,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    author='Jon Stutters',
    author_email='jstutters@jeremah.co.uk',
    description='An online colour naming experiment',
    url='colornaming.net',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='MIT',
    classifiers=[]
)
