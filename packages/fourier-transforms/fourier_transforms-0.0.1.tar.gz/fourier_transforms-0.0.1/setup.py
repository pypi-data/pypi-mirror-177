from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="fourier_transforms",
    version="0.0.1",
    author="Ygor",
    author_email="ygorbalves222@gmail.com",
    description="Fast Fourier Transform (FFT) and Discrete Fourier Transform (DFT) implementations",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ygorbalves/fft-dft-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)