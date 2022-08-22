import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="plex-file-organizer",
    version="1.0.0",
    author="Thiago Bedal",
    author_email="thiago.bedal@gmail.com",
    description=("A simple script to rename stinyk files on a plex server"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MilkyIQ/plex-file-organizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "rename = renamer.cli:main",
        ]
    }
)
