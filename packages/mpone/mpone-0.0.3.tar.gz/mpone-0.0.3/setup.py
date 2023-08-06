import os
from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md')) as f:
        long_description = f.read()
except Exception as e:
    long_description = "MPOne is a material physical toolbox."

setup(
    name="mpone",
    version="0.0.3",
    keywords=["VISA", "Material"],
    description="MPOne is more than One",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.10.0",
    license="MIT Licence",

    url="https://github.com/anine09/MPOne",
    author="Epsilon Luoo",
    author_email="epsilon_luoo@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    install_requires=["pyvisa", "pyvisa-py", "gpib-ctypes"],
    platforms="any"
)
