import setuptools
import unittest

with open("README.md", "r") as fh:
    long_description = fh.read()

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test/', pattern='*_test.py')
    return test_suite

setuptools.setup(
        name="dwf-sdk-python",
        version="0.1.1",
        author="Pei Zhongyi",
        author_email="peizhyi@gmail.com",
        description="DWF SDK in Python",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/thulab/dwf-sdk-python",
        packages=setuptools.find_packages(exclude=['test']),
        zip_safe=False,
        test_suite="dwf.test",
        classifiers=(
                "Programming Language :: Python :: 3.6",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
        ),
)
