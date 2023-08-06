from setuptools import setup
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tvmazetgbot",
    version="0.1.0",
    description="Demo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrei Y",
    author_email="andrkool151@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["tvmazetgbot", "tvmazetgbot.tvmaze"],
    include_package_data=True,
    install_requires=["pydantic==1.10.2"]
)
