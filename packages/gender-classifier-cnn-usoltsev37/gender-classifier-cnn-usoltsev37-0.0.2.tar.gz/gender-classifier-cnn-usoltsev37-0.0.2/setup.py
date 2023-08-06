import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "contourpy==1.0.6",
    "cycler==0.11.0",
    "fonttools==4.38.0",
    "kiwisolver==1.4.4",
    "matplotlib==3.6.2",
    "numpy==1.23.5",
    "packaging==21.3",
    "pandas==1.5.1",
    "Pillow==9.3.0",
    "pyparsing==3.0.9",
    "python-dateutil==2.8.2",
    "pytz==2022.6",
    "six==1.16.0",
    "torch==1.13.0",
    "torchaudio==0.13.0",
    "tqdm==4.64.1",
    "typing_extensions==4.4.0"
]

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    name="gender-classifier-cnn-usoltsev37",
    version="0.0.2",
    author="Nikita Usoltsev",
    author_email="nikitav030301@gmail.com",
    description="hse-engineering-practices-gender-classifier-cnn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usoltsev37/hse-engineering-practices-ml/tree/main/gender-classifier-cnn",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.9.12",
)