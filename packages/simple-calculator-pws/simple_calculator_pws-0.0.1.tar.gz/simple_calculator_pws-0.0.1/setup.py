from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="simple_calculator_pws",
    version="0.0.1",
    author="Paulo William",
    author_email="ziunewill@gmail.com",
    description="Calculadora básica para demonstração de criação de pacote",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PauloWilly/DIO_Projetos/Criacao_Pacotes_Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)