from setuptools import setup, find_packages

VERSION = '1.3'
DESCRIPTION = 'Email application'
LONG_DESCRIPTION = 'It is used for sending emails to multiple receivers at once.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="bread-mail",
    version=VERSION,
    author="leox",
    author_email="leox9611@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    package_data={"assets": ["*.png", "*.jpeg"]},
    zip_safe=False,
    # add any additional packages that
    install_requires=[],
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'email'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
