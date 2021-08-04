from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="draviz",
    version="0.1",
    packages=["src"],
    url="https://github.com/fredriko/data-readiness-assessment",
    license="MIT",
    author="Fredrik Olsson",
    author_email="fredrik.olsson@gmail.com",
    description="A program for visualizing the data readiness of NLP projects.",
    install_requires=["pandas", "plotly"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["draviz=src.draviz:main"]},
    long_description=long_description
)
