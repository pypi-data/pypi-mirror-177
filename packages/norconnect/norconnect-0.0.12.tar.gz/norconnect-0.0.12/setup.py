from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.12'
DESCRIPTION = 'Cloud Simplify is a package for handling aws services with simple functions '
LONG_DESCRIPTION = 'A package that allows to build application with different cloud providers with ease.'

# Setting up
setup(
    name="norconnect",
    version=VERSION,
    author="R Sanjeev Rao",
    author_email="sanjeevrao.159.v@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['boto3'],
    keywords=['python', 'AWS', 'aws', 'simplify', 'simplifyaws'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)