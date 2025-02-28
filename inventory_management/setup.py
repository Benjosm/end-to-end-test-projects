from setuptools import setup, find_packages

setup(
    name="inventory_management",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.3.3",
        "SQLAlchemy>=2.0.20",
        "pyjwt>=2.8.0",
        "pandas>=2.1.0",
        "marshmallow>=3.20.1",
        "click>=8.1.7",
        "python-dotenv>=1.0.0",
        "bcrypt>=4.0.1",
        "email-validator>=2.0.0",
    ],
    python_requires=">=3.9",
)
