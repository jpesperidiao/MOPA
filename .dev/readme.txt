Folder to accommodate dev tools for MOPA.

==============
Contents Tree
-- .dev
	-- testing_data
		-- ASTGTM2_N39W096
			+ ASTGTM2_N39W096_dem.tif
			+ ASTGTM2_N39W096_num.tif
			+ README.pdf
		-- sf-23-z-b
			+ rj_srtm_90m_sirgas2000-23s.tif
			+ SF-23-Z-B.tif
		-- utah
			+ 40112f1.dem
			+ 40112f1.dem.tif
			+ utah_lake_sirgas2000.tif
	-- venv (* does not come with the project)
		:: Directory containing Python3's virtual environment. Should be create ::
		:: whenever a clone is made from GitHub.                                ::
	+ originalScript.py
	+ requirements.txt
		:: List of MOPA'S Python3 package dependencies.                         ::
	+ readme.txt
==============

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