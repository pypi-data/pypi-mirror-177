import os
import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

LONG_DESCRIPTION = (HERE / "pypi.md").read_text()


REQUIREMENTS = [
    "requests"
]


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="streaming-logs",
    version=get_version("streaminglogs/__init__.py"),
    author="Location World",
    author_email="info@location-world.com",
    license="MPL-2.0",
    description="Streaming Logs SDK 4 Python.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://location-world@dev.azure.com/location-world/Research%20and%20Development/_git/streaming-logs.py',
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    python_requires='>=3.6'
)
