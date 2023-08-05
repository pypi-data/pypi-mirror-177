from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='itpy',
    version='0.0.1',
    packages=setup.find_packages(),
    url='-',
    license='MIT',
    author='Muhang Lan',
    author_email='mhlan95@163.com',
    description='Deep learning utils for information theory research',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
