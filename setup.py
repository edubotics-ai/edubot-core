from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dl4ds_tutor",
    version="0.1.0",
    packages=find_packages(),
    package_dir={"modules": "modules"},
    python_requires=">=3.7",
    install_requires=requirements,
    description="A Deep Learning for Data Science Tutor application",
)
