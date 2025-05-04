"""
Setup script for BitNet Virtual Co-worker Builder.
"""

from setuptools import setup, find_packages

setup(
    name="bitnet_vc_builder",
    version="0.2.0",
    description="A powerful and efficient AI virtual co-worker framework built on top of BitNet's 1-bit quantized language models",
    author="BitNet Virtual Co-worker Builder Team",
    author_email="example@example.com",
    url="https://github.com/bitnet/bitnet-vc-builder",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
        "requests>=2.25.0",
        "tqdm>=4.60.0",
        "pyyaml>=6.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "mypy>=0.812",
            "flake8>=3.9.2",
        ],
        "ui": [
            "streamlit>=1.0.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "bitnet-vc=bitnet_vc_builder.main:main",
        ],
    },
)
