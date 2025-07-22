
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load dataset
df = pd.read_csv("ml.csv")  # replace with your file
print("Initial Data:\n", df.head())

# Check missing values
print("\nMissing values:\n", df.isnull().sum())

# Visualize missing Y values
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("Missing Value Heatmap")
plt.show()

# Separate rows with and without missing Y
df_missing = df[df['Y'].isnull()]
df_not_missing = df[df['Y'].notnull()]

# --------------------------
# 1. Mean Imputation
df_mean = df.copy()
mean_value = df_mean['Y'].mean()
df_mean['Y'].fillna(mean_value, inplace=True)
print("\nMean Imputation:\n", df_mean['Y'].head())

# --------------------------
# 2. Median Imputation
df_median = df.copy()
median_value = df_median['Y'].median()
df_median['Y'].fillna(median_value, inplace=True)
print("\nMedian Imputation:\n", df_median['Y'].head())

# --------------------------
# 3. Mode Imputation
df_mode = df.copy()
mode_value = df_mode['Y'].mode()[0]
df_mode['Y'].fillna(mode_value, inplace=True)
print("\nMode Imputation:\n", df_mode['Y'].head())

# --------------------------
# 4. KNN Imputation
knn_imputer = KNNImputer(n_neighbors=3)
df_knn = pd.DataFrame(knn_imputer.fit_transform(df), columns=df.columns)
print("\nKNN Imputation:\n", df_knn['Y'].head())

# --------------------------
# 5. Linear Regression Imputation
# We will train a model using rows where Y is not null and predict the missing Y values.

df_lr = df.copy()
train_data = df_lr[df_lr['Y'].notnull()]
test_data = df_lr[df_lr['Y'].isnull()]

X_train = train_data.drop('Y', axis=1)
y_train = train_data['Y']
X_test = test_data.drop('Y', axis=1)

# Check if regression is appropriate (check correlation)
correlations = df.corr()['Y'].drop('Y')
print("\nCorrelation with Y:\n", correlations)

if correlations.abs().max() > 0.3:
    print("\nStrong enough correlation found. Applying Linear Regression Imputation...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    df_lr.loc[df_lr['Y'].isnull(), 'Y'] = y_pred
    print("\nLinear Regression Imputed Values:\n", df_lr.loc[df_lr['Y'].isnull(), 'Y'])
else:
    print("Correlation too weak. Linear Regression might not be appropriate.")

# --------------------------
# Optional: Compare distributions
plt.figure(figsize=(10, 6))
sns.kdeplot(df_not_missing['Y'], label="Original", fill=True)
sns.kdeplot(df_mean['Y'], label="Mean", fill=True)
sns.kdeplot(df_knn['Y'], label="KNN", fill=True)
sns.kdeplot(df_lr['Y'], label="Linear Regression", fill=True)
plt.title("Distribution of Imputed Y Values")
plt.legend()
plt.show()
