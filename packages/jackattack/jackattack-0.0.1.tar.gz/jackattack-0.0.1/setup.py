
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()


setup(
        name='jackattack', # this is what you 'pip install'
        version='0.0.1',
        description='An attack class for Jack',
        py_modules=["jackattack"], # this is what you will import
        package_dir={'': 'src'},
        classifiers=[ # tags used to search the library on PyPi
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Jack McShane",
        author_email="jackrmcshane@gmail.com",
        url="https://github.com/jackrmcshane/jackattack",
)
