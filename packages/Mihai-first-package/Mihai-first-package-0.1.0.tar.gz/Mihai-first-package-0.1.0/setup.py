from setuptools import setup

setup(
    name="Mihai-first-package",
    version="0.1.0",
    author="Avram Mihai",
    author_email="railgundrop@gmail.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first time when i made my own package"
)