from setuptools import setup, find_packages

VERSION = '1.4.1'
DESCRIPTION = 'Email application'
LONG_DESCRIPTION = 'This is a simple package that is used for sending email to multiple recipients at once.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="bread_mail",
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
    install_requires=['pandas', 'pyIsEmail', 'yagmail', 'Pillow'],
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
