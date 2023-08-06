from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
description = (this_directory/"README.md").read_text()

setup(
    name="Bogdan-first-own-package",
    version="0.2.0",
    description="This is my frist package",
    long_description=description,
    long_desciption_content_type="text/markdown",
    author="Bogdan-BF",
    author_email="b0gdan4x@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True
)