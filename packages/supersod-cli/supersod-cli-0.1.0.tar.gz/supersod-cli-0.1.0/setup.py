from setuptools import setup, find_packages

setup(
    name='supersodcli',
    version='0.1.-',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'keyring',
        'pyonfleet'
    ],
    entry_points={
        'console_scripts': [
            'supersod = src.supersodcli:cli',
        ],
    },
)