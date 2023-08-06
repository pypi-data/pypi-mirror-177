import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="om_simple_encoder",
    packages = find_packages(),
    package_data={'om_simple_encoder': ['*.jpg','*.gz']},
    include_package_data=True,
    version="0.1.3",
    author="kyusonglee",
    description="OM Simple Encoder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        #"matplotlib",
        #"opencv-python-headless<4.3",
        "Image",
        #"torch",
        #"torchvision",
        "pytorch-lightning",
        "timm",
        #"regex",
        #"ftfy",
        #"tqdm"
    ]
)
