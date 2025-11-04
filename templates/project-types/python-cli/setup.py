from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{{project_name}}",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A production-ready Python CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/{{project_name}}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "pydantic>=2.5.3",
        "pydantic-settings>=2.1.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "ruff>=0.1.11",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "{{command_name}}=cli.main:cli",
        ],
    },
)
