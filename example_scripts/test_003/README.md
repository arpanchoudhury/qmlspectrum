Same as `test_002` but after prediction confidence score in prediction (in %) is calculated.   

For the first molecule in the training example, the confidence score close to 100%

For the out-of-sample molecule (`iquery=5000`, index=5000 after shuffling) it turns out to be slightly low.

In one instance of shuffling, these were the scores obtained

```
Confidence score for entry  0 =  98.99813417950418  %
Confidence score for entry  5000 =  74.20354724832409  %
```
