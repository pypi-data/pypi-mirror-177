import setuptools


setuptools.setup(
    # Here is the module name.
    name="russian_protowhat",

    # version of the module
    version="0.0.1",

    # Name of Author
    author="nikitqa",

    # your Email address
    author_email="investinlipetsk@gmail.com",

    # #Small Description about module
    # description="adding number",

    # long_description=long_description,

    # Specifying that we are using markdown file for description
    # long_description=long_description,
    long_description_content_type="text/markdown",

    # if module has dependencies i.e. if your package rely on other package at pypi.org
    # then you must add there, in order to download every requirement of package

    #     install_requires=[
    #      "package1",
    #    "package2",
    #    ],
    python_requires='>=3.9',

    license="MIT",

    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3.9.0",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)