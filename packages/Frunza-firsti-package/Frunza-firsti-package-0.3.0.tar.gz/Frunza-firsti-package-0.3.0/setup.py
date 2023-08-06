from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
description = (this_directory/"README.md").read_text()

setup(
    name="Frunza-firsti-package",
    version="0.3.0",
    author="Cosofret Bogdan",
    author_email= "cosofret.bogdan@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first packages",
    long_description=description,
    long_description_content_type = "text/markdown"
)
