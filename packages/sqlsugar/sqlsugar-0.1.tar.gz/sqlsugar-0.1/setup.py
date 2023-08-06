import os

from setuptools import setup

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="sqlsugar",
    description="Automatic migrations for SQLAlchemy",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Teemu",
    url="https://github.com/Teemu/sqlsugar",
    project_urls={
        "Issues": "https://github.com/Teemu/sqlsugar/issues",
        "CI": "https://github.com/Teemu/sqlsugar/actions",
        "Changelog": "https://github.com/Teemu/sqlsugar/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["sqlsugar"],
    install_requires=["sqlalchemy", "alembic"],
    extras_require={
        "test": ["pytest", "pre-commit", "pytest-sugar", "sqlmodel", "black", "isort"]
    },
    python_requires=">=3.7",
)
