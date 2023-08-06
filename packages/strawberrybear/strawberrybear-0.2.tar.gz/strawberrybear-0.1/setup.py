import setuptools

long_description = open('README.md',encoding='utf-8').read()



setuptools.setup(
    name="strawberrybear",
    version="0.1",
    author="crake404",
    author_email="2576104742@qq.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AE-W/school-work",
    packages=setuptools.find_packages(),
    install_requires=['Pillow>=5.1.0', 'numpy==1.14.4'],

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)