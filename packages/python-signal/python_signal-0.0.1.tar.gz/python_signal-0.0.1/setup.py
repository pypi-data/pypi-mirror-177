import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='python_signal',
    version="0.0.1",
    author="Yaşar Özyurt",
    author_email="blueromans@gmail.com",
    description='Python Signal Event Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blueromans/PythonSignal.git',
    project_urls={
        "Bug Tracker": "https://github.com/blueromans/PythonSignal/issues",
    },
    install_requires=['blinker==1.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['python_signal'],
    python_requires=">=3.6",
)
