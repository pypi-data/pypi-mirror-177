from setuptools import setup

setup(
    name="mircix-own-package",
    version="0.1.0",
    author="Mircea Surdoiu",
    author_email="mircea.surdoiu@gmail.com",
    packages=["my_own_package"],
    package_dir={"": "src/"},
    include_package_data=True,
    description="This is my first package"
)