import setuptools

setuptools.setup(
    name = "alphabetss",
    version="1.0",
    author="test",
    author_email="firekarl@sina.com",
    description="test",
    url="",
    packages=setuptools.find_packages(where='.'
                                      ,exclude=()
                                      ,include=('*')
                                      ),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ]
)