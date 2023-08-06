import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="News-Indonesia",
    version="0.1",
    author="Fauzi Kurniawan",
    author_email="fauzik354313@gmail.com",
    description="This package will display various news in Indenesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reinz-Stuff/News-Indonesia",
    project_urls={
        "Github": "https://github.com/Reinz-Stuff",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
