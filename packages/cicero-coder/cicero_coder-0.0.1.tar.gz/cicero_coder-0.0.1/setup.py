from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cicero_coder",
    version="0.0.1",
    author="Cícero Hitzschky",
    author_email=" ",
    description="Crypt and Decrypt words ans phrases by Caesar's Cipher",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CiceroHitzschky/Dio-DataScientistBootCamp/tree/master/DataScientist/Criando%20Pacotes%20e%20M%C3%B3dulos%20Python/cifracesar/CiceroCoder/cifraCesar",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
