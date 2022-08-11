#! /bin/bash


[ -d "eyecite/" ] && rm -rf eyecite/

curl https://storage.courtlistener.com/bulk-data/eyecite/tests/one-percent.csv.bz2 --output one-percent.csv.bz2

for var in "$@"
do
    echo "$var"
    git clone -b $var https://github.com/freelawproject/eyecite.git
    cp benchmark.py eyecite/
    cp one-percent.csv.bz2 eyecite/
    cd eyecite
    poetry install --no-dev
    poetry run python benchmark.py --branch $var
    cd ..
    rm -rf eyecite/
done
pwd
ls
echo "Now lets compare our files and generate a graph we can use"
cd outputs && ls
cd ../
poetry init --no-interaction
poetry add matplotlib pandas
poetry install --no-dev
poetry run python chart.py --branch1 $1 --branch2 $2

# Clean up and remove miscellaneous material
rm poetry.lock
rm pyproject.toml

cd outputs && ls


