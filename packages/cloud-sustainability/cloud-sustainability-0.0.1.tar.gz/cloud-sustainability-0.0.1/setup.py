import os
import shutil
from pathlib import Path

from setuptools import setup, find_packages
from pkg_resources import parse_requirements


def get_version() -> str:
    """
    Get the current version of the package
    :return: version as string
    """
    return Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), "src", "version")).read_text()


def get_install_requires(requirements_file: Path = None) -> list[str]:
    """
    Get required dependencies from requirements.txt file and return them as a list of strings
    :param requirements_file: requirements.txt file as Path
    :return: Required dependencies as a list of string
    """

    if requirements_file is None:
        requirements_file = Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt"))

    return list(map(str, parse_requirements(requirements_file.read_text())))


def get_setup_requires() -> list[str]:
    """
    Get required dependencies for setup and build
    :return: Required dependencies as a list of string
    """

    setup_requires = ["pytest", "pytest-html", "pytest-cov"]
    setup_requires.extend(get_install_requires())
    return setup_requires


def cleanup() -> None:
    if os.path.exists("./dist/"):
        shutil.rmtree("./dist/")
    if os.path.exists("./build/"):
        shutil.rmtree("./build/")
    if os.path.exists("./eggs/"):
        shutil.rmtree("./eggs/")


def setup_package():
    """
    Setup the package for installation, building or development.
    """
    cleanup()
    setup(
        name="cloud-sustainability",
        version="0.0.1",
        author="Mohamad Karam Kassem",
        author_email="karam.kass@gmail.com",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        # license=Path("LICENSE").read_text(),
        description="A library offers some utilities to explore cloud resources",
        # long_description=Path("README.md").read_text(),
        setup_requires=get_setup_requires(),
        install_requires=get_install_requires()
    )


if __name__ == "__main__":
    setup_package()
