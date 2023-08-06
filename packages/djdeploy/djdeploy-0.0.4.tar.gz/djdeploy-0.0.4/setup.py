import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='djdeploy',
    version='0.0.4',
    description='Django automate deployment',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ardevpk/djdeploy",
    project_urls = {
        "Bug Tracker": "https://github.com/ardevpk/djdeploy/issues",
    },
    author="Abdul Rehman",
    author_email="adnan1470369258@gmail.com",
    py_modules=['djdeploy'],
    package_dir={'': 'src'},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    install_requires=[
        'paramiko==2.12.0',
        'PyAutoGUI==0.9.53'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['djdeploy=djdeploy.index:main']
    },
)
