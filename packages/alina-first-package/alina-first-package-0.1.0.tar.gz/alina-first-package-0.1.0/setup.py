# aici ne trebuie o functie
from setuptools import setup

setup(
    name="alina-first-package",
    version="0.1.0",
    author="alina",
    author_email="alina0515@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first package"
)