from setuptools import setup, find_packages

VERSION = '1.1.5'

setup(
    name="gutils-python",
    version=VERSION,
    description='Grab Utilities',
    long_description=open('README.md').read(),
    author='chaofeng.ma',
    author_email='chaofeng.ma@grabtaxi.com',
    url='https://gitlab.myteksi.net/quality-assurance/doraemon',
    include_package_data=True,
    zip_safe=True,
    packages=find_packages(exclude=["tests"]),
    install_requires=open('requirements.txt').read().split('\n'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
