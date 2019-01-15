Folder to accommodate dev tools for MOPA

./venv/ - dir:
Contains a Python3 virtual environment

./dependecies.txt - file:
Should contain all dependencies. It is planned to have only Python3 package dependencies.

./test_scripts/ - dir:
Should contain every test used during project dev. It intends to be the start of some unit test, so it always should be structured as described below, inside of a folder ":/MODULE/CLASS/":
	* "METHOD.py": testing script
	* "parameters.json": method's parameters
	* ":/input_data/": all input data should be presented there.
	* ":/output/": expected output data.