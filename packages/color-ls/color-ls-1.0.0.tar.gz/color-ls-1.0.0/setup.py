import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


# def get_version(rel_path):
#     for line in read(rel_path).splitlines():
#         if line.startswith('__version__'):
#             delimiter = '"' if '"' in line else "'"
#             return line.split(delimiter)[1]
#     else:
#         raise RuntimeError("Unable to find version string.")

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('version_info'):
            import re
            match = re.search(r"\(\d+(,\s*\d+)+\)$", line)
            if match is not None:
                version_info = eval(match.group())
                return '.'.join(str(c) for c in version_info)
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="color-ls",
    version=get_version('colorls/__init__.py'),
    author="Romeet Chhabra",
    author_email="romeetc@gmail.com",
    description="Pure Python implementation of subset of ls command \
        with colors and icons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/compilation-error/colorls",
    project_urls={
        "Bug Tracker": "https://gitlab.com/compilation-error/colorls/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    package_data={'colorls': ['config/colorls.ini']},
    include_package_data=True,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "lx=colorls.colorls:main",
        ],
    },
    data_files=[('colorls/config', ['colorls/config/colorls.ini']),
                ],
)
