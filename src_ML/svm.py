import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

data = np.loadtxt("201005.csv",delimiter=",",dtype=float)