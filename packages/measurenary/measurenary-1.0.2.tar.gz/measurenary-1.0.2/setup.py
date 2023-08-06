import setuptools

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="measurenary",
    version="1.0.0",
    author="Muhammad Dwiki Ramdhani",
    author_email="dwikiramdhani53@gmail.com",
    description="A package to calculate and find the best similarity between binary data features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://measurenary.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(include=['measurenary']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.21.6',
        'pandas>=1.3.5',
        'scikit_learn',
        'setuptools>=42',
        'tqdm'
    ],
    test_suite='tests'
)
