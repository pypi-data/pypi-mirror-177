from setuptools import setup

setup(
    name="Bogdan-first-own-package",
    version="0.1.0",
    description="This is my frist package",
    author="Bogdan-BF",
    author_email="b0gdan4x@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True
)