from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
description = (this_directory/"README.md").read_text()
setup(
    name= "Marius_baraian",
    version="0.2.0",
    author= "Baraian Marius",
    author_email= "marius.baraian08@gmail.com",
    packages= ["my_own_package"],
    package_dir= {"":"src\\"},
    include_package_data= True,
    description= "This is my first package",
    long_description= description,
    long_descriptiion_content_type= "text/markdown"
)
