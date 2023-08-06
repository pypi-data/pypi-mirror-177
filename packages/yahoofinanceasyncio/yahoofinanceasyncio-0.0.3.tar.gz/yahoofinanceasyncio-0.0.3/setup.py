import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="yahoofinanceasyncio",
    version="0.0.3",
    description="Yahoo prices",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/yahoofinanceasyncio",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["yahoofinanceasyncio"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['numpy'],
    entry_points={
        "console_scripts": [
            "yahoofinanceasyncio=yahoofinanceasyncio.__main__:main",
        ]
    },
)
