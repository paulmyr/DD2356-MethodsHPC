import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

files = []
for p in Path('a3/ex5/dynamic/').glob('*.txt'):
    if p.stem.startswith('timings'):
        content = {}
        for line in p.read_text().splitlines():
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                if value == "":
                    value = np.nan
                    # raise Warning(f"No value found for key '{key}' in file '{p.name}'")
                content[key] = value
    files.append(content)

df = pd.DataFrame(files)

df.to_csv("a3/ex5/dynamic/data.csv")

