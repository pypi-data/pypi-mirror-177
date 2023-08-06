from setuptools import find_packages, setup

setup(
    name='labs-integration-fec-consumedlimit-soap',
    version='0.0.29',
    include_package_data=True,
    install_requires=['labs-integration-fec-lms'],
    packages=find_packages(),
    zip_safe=False,
    author="Kuber Mehrotra",
    author_email="kuber.mehrotra@kuliza.com",
)
