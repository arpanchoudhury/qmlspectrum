Train an FCHL-KRR machine with 100 examples from the bigQM7w dataset (UFF geometries and wB97XD/def2SVPD TDDFT spectra) and predict the electronic spectrum of a query molecule

To run this example, install `qmlspectrum` via `pip install qmlspectrum` and the dependencies

Run

```
  python3.6 inp.py
```

In the input script, `iquery=0` indicates that we want to predict the spectrum of the first molecule after shuffling. This molecule is a part of the trainingset, so we will be able to predict its spectrum very well as can be seen by the output spectrum shown below.

If you want to try another example for query, you can check the _absolute_ indices of the bigQM7w molecules in the file `shuffle_index.dat`