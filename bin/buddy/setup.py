import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="buddy",
    version="0.0.1",
    author="Russ Hyde",
    author_email="russ_hyde AT hotmail DOT com",
    description="A small example package",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="-",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
