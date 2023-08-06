from setuptools import setup, find_packages
import codecs
import os
 

VERSION = '0.0.8'
DESCRIPTION = 'sample SDK by Arawinz'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="arawinz_s_sdk",
    version=VERSION,
    author="Arawinz (Chethan Pasupuleti)",
    author_email="<chethanpss24@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'py-algorand-sdk', 'pytz'],
    keywords=['python', 'arawinz', 'algorand', 'sdk'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)