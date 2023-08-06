import os
from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="djacc",
    version="0.1.0",
    description="An extensible user-accounts application for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Abdul Rehman",
    author_email="adnan1470369258@gmail.com",
    url="https://github.com/ardevpk/djacc",
    project_urls = {
        "Bug Tracker": "https://github.com/ardevpk/djacc/issues",
    },
    
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=['accounts'],
    packages=find_packages("src"),
    package_data={
        'accounts': [
            'templates/accounts/*.html',
            ]
        },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Django>=3.8",
        'django-crispy-forms>=1.14.0',
        'django-utils-six'
        ],
)
