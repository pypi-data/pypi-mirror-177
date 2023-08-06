import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XTTOOLS",
    version="0.9",
    author="fengchuan",
    author_email="fengchuanhn@gmail.com",
    description="XTJsonResponse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fengchuan1021",
    packages=setuptools.find_packages(),
    install_requires=['sqlalchemy','pydantic','orjson'],
    entry_points={

    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)