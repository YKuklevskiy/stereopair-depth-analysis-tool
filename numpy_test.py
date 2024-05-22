import numpy as np

values = np.array([3,4,6,2,12,4,5,7,3,2,4,6,7,40])
print(values.mean())
print(np.quantile(values, 0.5))