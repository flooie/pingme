# Run with make development --file other/Makefile -e BRANCH=update-courts-reporters-db
# update-courts-reporters-db
# make development --file other/Makefile -e BRANCH=update-courts-reporters-db
# make development --
# make development -e ref1=update-courts-reporters-db ref2=main


# Ensure VERSION is set.
ifndef ref1
$(error BRANCH variable is not set. Use -e BRANCH=XYZ to proceed.)
endif


development:
	pwd
	git clone -b $(ref1) https://github.com/freelawproject/eyecite.git other/eyecite
	cd other/eyecite && poetry install
	cp other/benchmark.py other/eyecite/
	cp other/one-percent.csv.bz2 other/eyecite/
	cd other/eyecite && poetry add --extras=benchmark pandas
	cd other/eyecite && poetry add --extras=benchmark matplotlib
	poetry run python other/eyecite/benchmark.py --branch $(ref1)

developmenty:
	git clone -b $(ref1) https://github.com/freelawproject/eyecite.git eyecite
	poetry init --no-interaction
	poetry add typed-ast lxml pandas diff_match_patch reporters-db matplotlib regex courts-db pyahocorasick
	cp poetry.lock eyecite/
	cp pyproject.toml eyecite/
	cp benchmark.py eyecite/
	cp one-percent.csv.bz2 eyecite/
	poetry run python eyecite/benchmark.py --branch $(ref1)

developmentx:
	git clone -b $(ref1) https://github.com/freelawproject/eyecite.git eyecite
	cd eyecite && poetry install
	cp poetry.lock eyecite/
	cp pyproject.toml eyecite/
	cp benchmark.py eyecite/
	cp one-percent.csv.bz2 eyecite/
	poetry run python eyecite/benchmark.py --branch $(ref1)
	poetry add lxml pandas diff_match_patch reporters-db matplotlib regex courts-db pyahocorasick

other:
	cp benchmark.py eyecite/
	cp one-percent.csv.bz2 eyecite/
	&& poetry run python eyecite/benchmark.py --branch $(ref1)
	cp benchmark.py eyecite/
	cp one-percent.csv.bz2 eyecite/
	poetry init --no-interaction
	poetry install
	poetry run python eyecite/benchmark.py --branch $(ref1)
	poetry run python eyecite/benchmark.py --branch $(ref1)
	rm pyproject.toml
	chmod -R +w eyecite
	rm -rf eyecite
	git clone -b $(ref2) https://github.com/freelawproject/eyecite.git eyecite
	cd eyecite/
	cp benchmark.py eyecite/
	cp one-percent.csv.bz2 eyecite/
	poetry init --no-interaction
	poetry run python eyecite/benchmark.py --branch $(ref2)
	rm pyproject.toml
	chmod -R +w eyecite
	rm -rf eyecite
