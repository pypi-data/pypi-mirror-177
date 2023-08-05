import setuptools

setuptools.setup(
    name="picompress",
    version="3.2.0",
    description="python compression lib",
    packages=['picompress'],
    package_data={'picompress': ['so/*']},
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)

