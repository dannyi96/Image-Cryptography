import setuptools

with open("README.md", "r") as f:
   long_description = f.read()

setuptools.setup(
    name="rubikencryptor",
    version="1.0.10",
    author="Daniel Isaac",
    author_email="danielbcbs2@gmail.com",
    description="Image Cryptography Based on Rubix's Cube Principle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dannyi96/Image-Cryptography",
    packages=['rubikencryptor'],
    include_package_data=True,
    license='MIT',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
          'numpy>=1.20.2',
          'Pillow>=8.4.0',
      ],
)