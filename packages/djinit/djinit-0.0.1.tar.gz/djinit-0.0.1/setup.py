import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='djinit',
    version='0.0.1',
    description='Django project initialize',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ardevpk/djinit",
    project_urls = {
        "Bug Tracker": "https://github.com/ardevpk/djinit/issues",
    },
    author="Abdul Rehman",
    author_email="adnan1470369258@gmail.com",
    py_modules=['djinit'],
    include_package_data=True,
    # include_dirs=['templates',],
    package_data={
            'djinit': [
                'utilities/templates/*.html',
                'utilities/templates/app/*.html',
                'utilities/templates/includes/*.html',
                'utilities/templates/layouts/*.html',
                'utilities/templates/partials/*.html',
            ]
        },
    package_dir={'': 'src'},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    install_requires=[
        'Django>=3.8',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['djinit=djinit.index:main']
    },
)
