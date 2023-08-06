from setuptools import setup
with open("README.md", 'r') as fh:
    long_description = fh.read()
setup(
    name='agile_north_build_essentials',
    version='0.0.1',
    description="Python scripts to assist in setting up project dependencies in order to build and run projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["agile_north_build_essentials"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    url="https://github.com/agile-north/build-essentails",
    author="Stefan Venter",
    author_email="stefan@nrth.com",
    extras_require={
        "dev": [
            "pytest>=3.7"
        ]
    }
)