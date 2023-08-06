from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package-template-master",
    version="0.0.2",
    author="Gracielle",
    author_email="",
    description="My short description, because is an example of DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="",
    packages= find_packages(),
    
    install_requires=requirements,
    python_requires='>=3.8',
)