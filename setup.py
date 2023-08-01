import pathlib
from setuptools import setup, find_packages

appversion = "2.0.3"

here = pathlib.Path(__file__).parent.resolve()

with open(f"{here}/macprefs/__init__.py", "w", encoding="utf-8") as initpy:
    initpy.write(f'__version__ = "{appversion}"')

setup(
    name="macprefs",
    version=appversion,
    description="Backup and Restore your Mac System and App Preferences",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sijanc147/macprefs",
    author="Sean Bugeja",
    author_email="seanbugeja23@gmail.com",
    license="Unlicense",
    classifiers=[
        "License :: Public Domain",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["mac", "backup", "prefereces", "prefs"],
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=["mock"],
    extras_require={
        "dev": [
            "pylint",
            "pytest",
            "pytest-cov",
            "pytest-testmon",
            "pytest-watcher",
        ]
    },
    entry_points={
        "console_scripts": [
            "macprefs=macprefs.__main__:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/sijanc147/macprefs/issues",
        "Source": "https://github.com/sijanc147/macprefs",
    },
)
