import pandas as pd

pd1 = pd.DataFrame([1, 2, 3])
pd2 = pd.DataFrame([2, 2, 2])

print(pd.concat([pd1, pd2]))
