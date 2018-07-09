from setuptools import setup, find_packages

setup(
    name="BNO",
    version="0.0.1",
    install_requires=[
        "pyserial",
    ],
    packages=find_packages()
)
