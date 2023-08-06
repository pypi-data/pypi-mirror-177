from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'great tool to help you with your programming journy'

# Setting up
setup(
    name="RayTux",
    version=VERSION,
    author="Seartuxe (Ali Hadwan)",
    author_email="raytux.py@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['keyboard'],
    keywords=['python', 'password', 'keyboard_input'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)