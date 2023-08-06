from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
description = (this_directory/"README.md").read_text()
setup(
    name="Marius-firstpackage",
    version="0.2.0",
    author="Marius Mihai Neagu",
    author_email="marius.neagu828@gmail.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first package",
    long_description=description,
    long_description_content_type="text/markdown"
)
