import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="torchphm",
    version="1.1.9",
    author="police",
    author_email="criminal@qq.com",
    license='MIT',
    description="pick feature for phm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ultrapower_cd_2364839934_admin/phm_feature_torch",
    packages=setuptools.find_packages(),
    install_requires=['torch'],
    extras_require={'tests': ['pytest', 'librosa']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
