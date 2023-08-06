from setuptools import find_packages, setup


setup(
    name = "dtBotSDK",
    version ="1.0",
    packages = find_packages(),
    author = "arthurtung",
    license="LGPL",
    install_requires = ["requests"],
    zip_safe = False
)