import setuptools

with open("WeatherTracker/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WeatherTracker",
    version="0.0.1",
    author="Benjamin Ringel",
    author_email="<benringel22@gmail.com>",
    description="Personal project for tracking weather",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bringel2/WeatherTracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
