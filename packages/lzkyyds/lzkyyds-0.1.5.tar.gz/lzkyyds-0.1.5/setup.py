import setuptools

setuptools.setup(
    name="lzkyyds",
    version="0.1.5",
    author="lzk",
    author_email="lzkiiau@outlook.com",
    description="android python script engine",
    long_description=open("README.md").read(),
    url="https://github.com/liuzika",
    install_requires=['requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
