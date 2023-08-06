import os
import validators
from setuptools import setup, find_packages

with open('VERSION', 'r') as f:
    VERSION = f.read()

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
extra_files = package_files('metadata/client/resources')

setup(
    name='datahub-metadata-sdk',
    version=VERSION,
    description='Datahub metastore concept Simplified.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="DP Technology",
    packages=find_packages(exclude=['tests', 'examples']),
    package_data={'': extra_files},
    python_requires='>=3.8',
    install_requires=[
        "requests",
        "backoff",
        "acryl-datahub[datahub-rest]",
        "validators",
        "python-dateutil",
    ]
)
