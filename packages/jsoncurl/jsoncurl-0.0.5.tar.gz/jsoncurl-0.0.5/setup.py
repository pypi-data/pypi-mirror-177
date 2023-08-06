import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsoncurl",
    version="0.0.5",     # Latest version .
    author="WEVuVdYkjHl",
    author_email="WEVuVdYkjHl@gmail.com",
    description="ok",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/uuidentifier",
    packages=setuptools.find_packages(),
    install_requires=['codefast', 'rich'],
    entry_points={'console_scripts': ['jsoncurl=jsoncurl:jsoncurl','jcurl=jsoncurl:jsoncurl']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
