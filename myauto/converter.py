import pandas as pd
import json

df = pd.read_json("/Users/pc/Documents/GitHub/myauto-scraping-tool/data.jl", lines=True)
print(df.head(10))