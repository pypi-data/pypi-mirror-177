# PACKAGING

from setuptools import setup
import pathlib

# **** Metas ****
# Where am i
curr_dir = pathlib.Path(__file__).parent.resolve()
meta_dir = (curr_dir / "pcidevlib/meta")
# Description from the README.md
long_description = (curr_dir / "README.md").read_text(encoding="utf-8")
# Name
name = (meta_dir / "pname").read_text(encoding="utf-8")
# Version
version = (meta_dir / "version").read_text(encoding="utf-8")
# Description
description = (meta_dir / "description").read_text(encoding="utf-8")

# **** SETUP ****
setup(
	name=name,
	version=version,
	description=description,
	long_description=long_description,
	long_description_content_type="text/markdown",
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
		name
	],
	project_urls={
		"Source Code": "https://github.com/as43z/pci-dev-lib"
	}
)