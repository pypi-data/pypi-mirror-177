import os
import setuptools


with open("README.md", "r", encoding="UTF8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="standard-response-lib",
    version=os.getenv("GITHUB_REF_NAME", "v0.0.4"),
    author="Avikus",
    author_email="dev@avikus.ai",
    description="A response library package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avikus-ai/standard-response-lib",
    packages=setuptools.find_packages(exclude=("tests", "examples")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pydantic>=1.10.2"],
    python_requires=">=3.8",
)
