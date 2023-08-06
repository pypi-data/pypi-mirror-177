from setuptools import setup
from pathlib import Path

this_directory=Path(__file__).parent
description=(this_directory/"README.md").read_text()
setup(
    name="Mihai-first-package",
    version="0.2.0",
    author="Avram Mihai",
    author_email="railgundrop@gmail.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first time when i made my own package",
    long_description=description,
    long_description_content_type="text/markdown"
)