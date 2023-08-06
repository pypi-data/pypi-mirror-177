from setuptools import setup

setup(
    name="Marius-firstpackage",
    version="0.1.0",
    author="Marius Mihai Neagu",
    author_email="marius.neagu828@gmail.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first package"
)