from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='bashit',
    version='1.0.0',
    description='put stuff in a file and bash it',
    long_description_content_type="text/markdown",
    license="MIT",
    long_description=long_description,
    author='Dror Speiser',
    url="http://github.com/drorspei/bashit",
    packages=['bashit'],
    entry_points={
        'console_scripts': [
            'bashit = bashit.main:main',
        ],
    },
)
