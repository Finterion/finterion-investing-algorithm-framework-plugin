import setuptools
from version import get_version

VERSION = get_version()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="finterion investing algorithm framework",
    version=get_version(),
    license='Apache License 2.0',
    author="Finterion",
    description="Official Finterion plugin for the investing algorithm framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/finterion/finterion-investing-algorithm-framework.git",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    keywords=[
        'Finterion',
        'finterion',
        'investing-algorithm',
        'investing-algorithm-framework',
        'INVESTING',
        'BOT',
        'ALGORITHM',
        'FRAMEWORK',
        'investing-bots',
        'trading-bots'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development",
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=required,
    python_requires='>=3',
    include_package_data=True,
)
