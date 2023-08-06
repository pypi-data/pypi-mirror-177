from setuptools import setup

setup(
    name="Elena-first-package",
    version="0.1.0",
    author="Elena Kruger",
    author_email="elenaalinakruger@gmail.com",
    packages=["my_own_package"],
    package_dir={"":"src"},
    include_package_data=True,
    description="This is the first package by Elena"
)