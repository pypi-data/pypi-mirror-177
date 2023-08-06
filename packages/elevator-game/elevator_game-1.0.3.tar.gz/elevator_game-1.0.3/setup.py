import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elevator_game",
    version="1.0.3",
    author="Michael Smith",
    author_email="michael.smith.ok@gmail.com",
    description="A TUI game where you control elevators.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smwa/elevator_game",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
