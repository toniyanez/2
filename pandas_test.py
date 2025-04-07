import pandas as pd

manufacturing_locations = ["A", "B"]
market_locations = ["X", "Y"]

df = pd.DataFrame(index=manufacturing_locations, columns=market_locations)

# Try with .loc
df.loc["A", "X"] = {}
print("After .loc assignment:")
print(df)

# Reset and try with .iloc
df = pd.DataFrame(index=manufacturing_locations, columns=market_locations)
df.iloc[0, 0] = {}
print("\nAfter .iloc assignment:")
print(df)
