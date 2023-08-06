from setuptools import setup, find_packages

with open('VERSION', 'r') as f:
    VERSION = f.read()

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='datahub-metadata-sdk',
    version=VERSION,
    description='Datahub metastore concept Simplified.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="DP Technology",
    packages=find_packages(exclude='tests'),
    python_requires='>=3.8',
    install_requires=[
        "requests",
        "backoff",
    ]
)
