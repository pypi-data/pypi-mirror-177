from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'Generate domain name variations based on keywords and synonyms.'
LONG_DESCRIPTION = 'A package that allows you to easily generate a list of domain name variations based on keywords and synonyms.'

# Setting up
setup(
    name="domaingen",
    version=VERSION,
    author="GoInfosystems.com",
    author_email="<info@goinfosystems.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['python-whois', 'py-thesaurus', 'random-proxies'],
    keywords=['python', 'whois', 'domain', 'domain name', 'domain name registration', 'domain names', 'domains', 'dns'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)