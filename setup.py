from setuptools import find_packages, setup

setup(
    name="STACKMENTOR",
    version="0.0.1",
    author="Dogbalou Motognon Wastalas",
    author_email="wastalasdassise@gmail.com",
    packages=find_packages(),
    install_requires=['langchain-astradb','langchain ','langchain-openai','datasets','pypdf','python-dotenv','flask']
)