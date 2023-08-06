import setuptools
setuptools.setup(
    name="dir_sizer",                     # This is the name of the package
    version="0.0.5",                        # The initial release version
    author="Madhankumar",                     # Full name of the author
    description="Get the folder size using a base path",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
)