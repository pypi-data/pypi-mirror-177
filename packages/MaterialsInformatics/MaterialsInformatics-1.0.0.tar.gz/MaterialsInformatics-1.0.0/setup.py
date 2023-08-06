import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

desc = (
    "Clean and add extra information to data "
    + "..."
)

# This call to setup() does all the work
setup(
    name="MaterialsInformatics",
    version="1.0.0",
    packages=find_packages(exclude=("tests",)),
    description=desc,
    long_description=README,
    long_description_content_type="text/plain",
    url="https://github.com/PapStatMechMat/SeaPy",
    license="BSD",
        classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: BSD License",
                    "Operating System :: OS Independent",
                ],
        include_package_data=True,
        python_requires='>=3',
        install_requires=[
                    "numpy>=0.0",
                    "matplotlib>=0.0",
                    "opencv-python>=0.0",
                    "webcolors>0.0",
                    "scipy",
                    "sklearn",
                    "PyWavelets",
                ],
)
