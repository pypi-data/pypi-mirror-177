import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "woshi",
    packages = ["woshi"],
    version = "2.0.2",
    license="MIT",
    description = "On-the-go HTML Abstraction and Generator for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Rodney Maniego Jr.",
    author_email = "rodney.maniegojr@gmail.com",
    url = "https://github.com/rmaniego/woshi",
    download_url = "https://github.com/rmaniego/woshi/archive/v1.0.tar.gz",
    keywords = ["html", "abstraction", "template", "python"],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers", 
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.9"
)