rm -rf qmlspectrum.egg-info/
rm -rf dist/*
python setup.py sdist
python3.6 /Users/raghurama/anaconda3/lib/python3.6/site-packages/twine/__main__.py upload dist/*
