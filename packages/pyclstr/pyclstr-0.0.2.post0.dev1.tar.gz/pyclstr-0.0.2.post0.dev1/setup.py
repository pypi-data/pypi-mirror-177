
"""
@author: Chris Lockhart <clockha2@gmu.edu>
"""

from setuptools import setup
import versioneer


# Read in requirements.txt
with open('requirements.txt', 'r') as buffer:
    requirements = buffer.read().splitlines()

# Long description
with open('README.rst', 'r') as buffer:
    long_description = buffer.read()

# Setup
setup(
    name='pyclstr',
    version= versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Chris Lockhart',
    author_email='clockha2@gmu.edu',
    description='Simple clustering algorithms',
    long_description=long_description,
    url="https://www.lockhartlab.org/",
    packages=[
        'pyclstr',
    ],
    install_requires=requirements,
    include_package_data=True,
    zip_safe=True,
)
