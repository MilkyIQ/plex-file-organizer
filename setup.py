import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="plex-file-organizer",
    version="1.0.0",
    author="Thiago Bedal",
    author_email="thiago.bedal@gmail.com",
    description=("fuck you."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="dontgiveashit",
    project_urls={
        "Bug Tracker": "stfu",
    },
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
