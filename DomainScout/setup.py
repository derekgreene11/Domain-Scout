from setuptools import setup, find_packages
from setuptools.command.install import install
import os

setup(
    name='DomainScout',
    version="1.0",
    author="Derek R. Greene",
    author_email="derek@derekrgreene.com",
    description="A desktop GUI client to view discovered domains using known disposable emails in WHOIS contact records.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://",
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyQt6',
        'python-dotenv',
        'python-whois',
    ],
    include_package_data=True,
    data_files=[('icons', ['domainscout/appicon.ico'])],
    entry_points={
        'console_scripts': [
            'domainscout = domainscout.GUI:main'
        ]
    }
)
