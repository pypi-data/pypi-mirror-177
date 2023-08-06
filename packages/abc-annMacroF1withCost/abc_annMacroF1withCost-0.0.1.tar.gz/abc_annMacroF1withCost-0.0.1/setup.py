from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='abc_annMacroF1withCost',
    version='0.0.1',
    description='ABC-ANN-MacroF1withCost is a classification method that combines ABC algorithm with a artificial neural network classification model',
    py_modules=['abc_annMacroF1withCost'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kagandedeturk/ABC-ANN-MacroF1withCost",
    author="Bilge Kagan Dedeturk",
    author_email="kagandedeturk@gmail.com",
)
