import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(

    name="IndonesiaLatestEarthQuakeAlert",
    version="0.0.6",
    author="M Soleh Fajari",
    author_email="<m.soleh.fajari@gmail.com>",
    description="This package will guide us get earth quake information from bmkg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fajari/Indonesia-Eartquake-Alert",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)