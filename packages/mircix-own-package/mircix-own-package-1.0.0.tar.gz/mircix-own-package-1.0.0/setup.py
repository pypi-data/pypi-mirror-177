from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
description = (this_directory/"README.md").read_text()

setup(
    name="mircix-own-package",
    version="1.0.0",
    author="Mircea Surdoiu",
    author_email="mircea.surdoiu@gmail.com",
    packages=["my_own_package"],
    package_dir={"": "src/"},
    include_package_data=True,
    description="This is my first package",
    long_description=description,
    long_description_content_type="text/markdown"
)
