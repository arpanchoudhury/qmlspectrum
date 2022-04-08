Same as `test_003b` but the model will be trained directly on oscillator strengths. 

Both ML-predicted and TDDDFT oscillator strength vectors are divided by their sums to estimate the confidence score.

These are the changes in the `inp.py` 

```
line-2    import numpy as np
```

We will divide the oscillator strengths by the sum over all bins
```
 57 #=== prediction
 59 iquery=0
 62 Int_pred=Int_pred/np.sum(Int_pred)
 63 Int_TDDFT=Int_TDDFT/np.sum(Int_TDDFT)
 66 
 67 iquery=5000
 70 Int_pred=Int_pred/np.sum(Int_pred)
 71 Int_TDDFT=Int_TDDFT/np.sum(Int_TDDFT)
```

The resulting confidence scores are very similar to values from `test_003a`

```
Confidence score for entry  0 =  99.0216915151149  %
Confidence score for entry  5000 =  73.93701467824154  %
```
