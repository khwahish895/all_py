import pandas as pd
from sklearn.linear_model import LinearRegression

# Step 1: Load the dataset
df = pd.read_csv("ml1.csv")
print("Original Dataset with Missing Y:\n", df)

# Step 2: Split into rows with and without missing Y
df_missing = df[df['Y'].isnull()]
df_not_missing = df[df['Y'].notnull()]

# Step 3: Prepare training data
X_train = df_not_missing.drop("Y", axis=1)
y_train = df_not_missing["Y"]

# Step 4: Prepare test data (where Y is missing)
X_test = df_missing.drop("Y", axis=1)

# Step 5: Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 6: Predict missing Y values
y_pred = model.predict(X_test)

# Step 7: Fill predicted values back into the original dataframe
df.loc[df['Y'].isnull(), 'Y'] = y_pred

# Step 8: Show updated dataset
print("\n✅ Updated Dataset with Predicted Y values:\n", df)
