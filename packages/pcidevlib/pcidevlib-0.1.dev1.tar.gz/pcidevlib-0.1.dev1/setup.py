# PACKAGING

from setuptools import setup
import pathlib

# **** Long-description ****
# Where am i
curr_dir = pathlib.Path(__file__).parent.resolve()
# Description from the README.md
long_description = (curr_dir / "README.md").read_text(encoding="utf-8")

# **** SETUP ****
setup(
	name="pcidevlib",
	version="0.1.dev1",
	description="Custom PCI device utils for reading writing.",
	long_description=long_description,
	long_description_type="text/markdown",
	url="https://github.com/as43z/pci-dev-lib",
	author="Albert Sáez Núñez",
	author_mail="albert.saez.nunez@estudiantat.upc.edu",
	classifiers=[
		"Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License"
	],
	keywords="setuptools, pci, device, mmio, memory",
	python_requires=">=3.7, <4",
	# Package
	packages=[
		"src"
	],
	project_urls={
		"Source Code": "https://github.com/as43z/pci-dev-lib"
	}
)