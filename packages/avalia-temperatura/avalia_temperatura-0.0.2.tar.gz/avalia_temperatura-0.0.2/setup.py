from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="avalia_temperatura",
    version="0.0.2",
    author="Gabriel",
    description="Este pacote é um exercício do Desafio de Projeto da DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GabeGD/Bootcamp_Geracao_Tech_Unimed_BH_Ciencia_de_Dados/pacote_DIO",
    packages=find_packages(),
    python_requires='>=3.8',
)