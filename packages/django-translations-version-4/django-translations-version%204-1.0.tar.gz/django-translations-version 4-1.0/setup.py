import setuptools
import json


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("config.json", "r") as fh:
    info = json.load(fh)


setuptools.setup(
    name=info["project"]["dist"],
    version=info["release"]["name"],
    description=info["project"]["desc"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bbmokhtari.github.io/django-translations/",
    author=info["author"]["name"],
    author_email=info["author"]["email"],
    classifiers=[
        "Development Status :: " + info["release"]["classifier"],
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Internationalization",
    ],
    keywords=" ".join(info["keywords"]),
    project_urls={"Documentation": "https://bbmokhtari.github.io/django-translations/"},
    packages=setuptools.find_packages(
        exclude=[
            "sample",
            "sample.migrations",
            "tests",
        ]
    ),
    python_requires=">=3.6, <=4",
)
