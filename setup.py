from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in qubix_custom/__init__.py
from qubix_custom import __version__ as version

setup(
	name="qubix_custom",
	version=version,
	description="Test",
	author="test",
	author_email="test",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
