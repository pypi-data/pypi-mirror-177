from setuptools import setup

setup(
    name="Frunza-firsti-package",
    version="0.2.0",
    author="Cosofret Bogdan",
    author_email= "cosofret.bogdan@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first packages"
)
