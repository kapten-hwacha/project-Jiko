import numpy as np
import pandas as pd

map_excel = pd.read_excel("jiko_map.xlsx", header=None)
map = map_excel.values
print(map)
print(type(map))


