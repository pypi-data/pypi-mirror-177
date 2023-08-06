from setuptools import setup, find_packages
with open("requirements.txt", "r") as fh:
    requirements = fh.read()
setup(name = "fakeapistories",
version = 0.1,
author = "Rohan",
author_email = "rohansomkuwar97@gmail.com",
description = "This code is fetching data through the fakedata api",

url = "https://github.com/rohan-somkuwar/clitool/tree/master",
py_modules = ['fakeapistories'],
packages = find_packages(),
install_requires = [requirements],
python_requires = ">=3.7",
classifiers = [
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
entry_points = """
[console_scripts]

"""
)