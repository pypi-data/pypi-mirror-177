from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="high_pass_filters",
    version="0.0.1",
    author="Leonardo",
    author_email="leonardo.costa.sousa84@aluno.ifce.edu.br",
    description="high-pass filter package using Sobel and Prewitt",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leo22080/hpf-package-sobel-prewitt.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)