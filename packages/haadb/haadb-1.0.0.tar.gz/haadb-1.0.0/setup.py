import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "haadb",
    packages = ["haadb"],
    version = "1.0.0",
    license="MIT",
    description = "Hive-as-a-DB SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Rodney Maniego Jr.",
    author_email = "rodney.maniegojr@gmail.com",
    url = "https://github.com/rmaniego/haadb",
    download_url = "https://github.com/rmaniego/haadb/archive/v1.0.tar.gz",
    keywords = ["haadb", "hive", "blockchain", "api", "sdk", "database"],
    install_requires=["hive-nektar", "cryptography"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers", 
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.9"
)