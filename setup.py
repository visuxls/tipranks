import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="tipranks",
	version="0.0.5",
	author="visuxls",
	description="Python interface to communicate with TipRanks API.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	py_modules=["tipranks"],
	install_requires=["requests"]
)