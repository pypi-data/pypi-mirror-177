# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open

# This call to setup() does all the work
setup(
    name="automation-helper",
    version="0.0.10",
    description="automation helper library",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='juan matias tulli',
    author_email='jmatiastulli@gmail.com',
    license="jmt",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    py_modules=["logger", "db_connector", "kpi", "config", "reports_utils"],
    include_package_data=True,
    install_requires=["pandas", "psycopg2", "datetime", "configparser"]
)
