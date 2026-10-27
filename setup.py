from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="safecrime",
    version="1.0.0",
    author="SafeVision Analytics Team",
    author_email="contact@safevision.org",
    description="A Python Data Science and Machine Learning Library for Crimes Against Women Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vinayakbhatia22/Women-crime-detection",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.2.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
    ],
    entry_points={
        "console_scripts": [
            "safecrime-pipeline=safecrime.pipeline:main",
        ],
    },
)
