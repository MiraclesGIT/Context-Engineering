"""
Context Engineering Package Setup
=================================

Setup configuration for the Context Engineering package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

# Get version from __init__.py
def get_version():
    """Extract version from __init__.py"""
    init_file = os.path.join(os.path.dirname(__file__), "__init__.py")
    with open(init_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="context-engineering",
    version=get_version(),
    author="Context Engineering Contributors",
    author_email="contact@context-engineering.org",
    description="A comprehensive contextual AI engine integrating cutting-edge research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/context-engineering/context-engineering",
    project_urls={
        "Bug Tracker": "https://github.com/context-engineering/context-engineering/issues",
        "Documentation": "https://context-engineering.readthedocs.io/",
        "Source Code": "https://github.com/context-engineering/context-engineering",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "asyncio",
        "dataclasses",
        "typing-extensions",
        "pyyaml>=5.4.0",
        "psutil>=5.8.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=21.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
            "isort>=5.9.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.12.0",
        ],
        "examples": [
            "jupyter>=1.0.0",
            "matplotlib>=3.5.0",
            "plotly>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "context-engine=context_engineering.cli:main",
            "ce-examples=context_engineering.examples:run_all_examples",
        ],
    },
    include_package_data=True,
    package_data={
        "context_engineering": [
            "config/*.yaml",
            "config/*.json", 
            "templates/*.py",
            "examples/*.py",
        ],
    },
    zip_safe=False,
    keywords=[
        "artificial-intelligence",
        "machine-learning",
        "natural-language-processing",
        "cognitive-computing",
        "context-engineering",
        "neural-fields",
        "memory-systems",
        "symbolic-processing",
        "quantum-semantics",
        "progressive-complexity",
    ],
)