import pathlib
from setuptools import setup, find_packages


def test_suite():
    import unittest

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="scinode-app",
    version="0.2.0",
    description="Design computational workflow using nodes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/scinode/scinode-app",
    author="Xing Wang",
    author_email="xingwang1991@gmail.com",
    license="MIT License",
    classifiers=[],
    packages=find_packages(),
    entry_points={},
    install_requires=["flask", "scinode", "numpy", "click"],
    # package_data={},
    include_package_data=True,
    python_requires=">=3.6",
    test_suite="setup.test_suite",
)
