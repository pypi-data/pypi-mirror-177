from setuptools import setup
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='UFANET',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author='Yuqi Fang',
    author_email='yuqi9199@gmail.com',
    description='UFA-Net method proposed in paper Unsupervised Cross-Domain Functional MRI Adaptation for Automated Major Depressive Disorder Identification',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy', 'torch', 'torchvision', 'scikit_learn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
