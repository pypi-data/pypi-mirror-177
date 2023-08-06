from setuptools import setup


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


setup(
    name="delphai-ml-utils",
    version="1.0.6",
    description="A Python package to manage delphai machine learning operations.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/delphai/delphai-ml-utils",
    author="ml-team-delphai",
    author_email="ml@delphai.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ml_utils"],
    include_package_data=True,
    install_requires=[
        "omegaconf",
        "azure-storage-blob",
        "bson",
        "coloredlogs",
        "confuse",
        "google",
        "gspread",
        "motor",
        "nlpaug",
        "nltk",
        "numpy",
        "pandas",
        "pysbd",
        "python-dotenv",
        "scikit-learn",
        "tldextract",
        "torch",
        "tqdm",
        "transformers",
        "transformers[onnx]",
    ],
)
