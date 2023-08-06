import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyconl",
    version="0.4.1",
    author="Jara van Veldhoven",
    author_email="jarav@nveldhoven.nl",
    description="Python bibliotheek voor Constructief Ontwerpen.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ornor/pyco",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)