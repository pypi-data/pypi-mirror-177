from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'basic hello package'

# Setting up
setup(
    name="hello-ta2642",
    version=VERSION,
    description=DESCRIPTION,
    long_description= long_description,
    long_description_content_type = "text/markdown",
    py_modules=["hello"],
    package_dir={'': 'src'},
    url = "https://github.com/tamanna-a/package",
    author= "Tamanna",
    author_email="ta2642@columbia.edu",
    install_requires = [
        "blessings ~=1.7",
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public "
        "License v2 or later (GPLv2+)"

    ]
)