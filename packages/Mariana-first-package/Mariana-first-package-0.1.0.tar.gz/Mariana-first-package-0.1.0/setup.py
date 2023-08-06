from setuptools import setup

setup(
    name="Mariana-first-package",
    version="0.1.0",
    author="Mariana Balan",
    author_email="marianabalan78@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src"},
    include_package_data=True,
    description="This is my first time when I made my own package"
)