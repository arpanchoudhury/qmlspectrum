Same as `test_002` but after prediction confidence score in prediction (in %) is calculated. We will also remove the lines for making the plots.   

These are the changes in the `inp.py` 

```
line-2    import numpy as np
```

We will divide the oscillator strengths by the sum over all bins
```
line-43    for i_mol in range(N_mol):
line-44        Int_lam[i_mol,:]=Int_lam[i_mol,:]/np.sum(Int_lam[i_mol,:])
```

We will calculate the confidence score  
```
line-65    phi=qmlspectrum.confidence_score(Int_pred, Int_TDDFT)
line-66    print('Confidence score for entry ', iquery,'= ',phi, ' %')
```

```
line-71    phi=qmlspectrum.confidence_score(Int_pred, Int_TDDFT)
line-72    print('Confidence score for entry ', iquery,'= ',phi, ' %')
```

For the first molecule in the training example, the confidence score close to 100%

For the out-of-sample molecule (`iquery=5000`, index=5000 after shuffling) it turns out to be slightly low.

In one instance of shuffling, these were the scores obtained

```
Confidence score for entry  0 =  98.99813417950418  %
Confidence score for entry  5000 =  74.20354724832409  %
```
