from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package-image-template_processing_2",
    version="0.0.1",
    author="LucimarN",
    author_email="lucimar.neves@gmail.com",
    description="Template packages",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucimarNeves/package-template-image_dio",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)