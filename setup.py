from setuptools import setup, find_packages

setup(
    name="adblocker-backend",
    version="1.0.0",
    description="Professional Ad Blocker Browser Extension Backend",
    author="AdBlocker Team",
    python_requires=">=3.11",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[
        "fastapi>=0.111.0",
        "uvicorn[standard]>=0.29.0",
        "httpx>=0.27.0",
        "requests>=2.31.0",
        "pandas>=2.2.2",
        "numpy>=1.26.4",
        "scikit-learn>=1.4.2",
        "APScheduler>=3.10.4",
        "sqlalchemy>=2.0.30",
        "alembic>=1.13.1",
        "pydantic>=2.7.1",
        "pydantic-settings>=2.2.1",
        "python-dotenv>=1.0.1",
        "aiofiles>=23.2.1",
        "slowapi>=0.1.9",
        "tldextract>=5.1.2",
        "joblib>=1.4.2",
    ],
    extras_require={
        "dev": [
            "pytest>=8.2.0",
            "pytest-asyncio>=0.23.6",
            "pytest-cov>=5.0.0",
            "black>=24.4.2",
            "flake8>=7.0.0",
            "mypy>=1.10.0",
        ]
    },
    entry_points={"console_scripts": ["adblocker=run:main"]},
)
