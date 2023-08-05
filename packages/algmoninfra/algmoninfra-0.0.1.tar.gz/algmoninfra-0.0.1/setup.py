import setuptools

with open("README.md", "r",encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algmoninfra",
    version="0.0.1",
    author="algmon",
    author_email="support@algmon.com",
    description="the algmon infra python lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
