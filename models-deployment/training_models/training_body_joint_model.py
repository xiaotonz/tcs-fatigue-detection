import pandas as pd
import glob
from joblib import dump


# Path to the directory containing the CSV files
csv_directory = 'body_joint_model_fatigue_detection_csv_data/*.csv'

# Use glob to get a list of all CSV files in the directory
csv_files = glob.glob(csv_directory)

# Initialize an empty list to store DataFrames
dfs = []

# Iterate through the CSV files and read them into DataFrames
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

combined_df.head()

combined_df.shape

combined_df.drop(combined_df.columns[0], axis=1, inplace=True)

# Shuffle the rows
shuffled_df = combined_df.sample(frac=1, random_state=42)

# Display the shuffled DataFrame
shuffled_df.head()

import pandas as pd

# Assuming you have a DataFrame called 'df'
# Check for null values in each column
null_values = shuffled_df.isnull().sum()

# Display the count of null values for each column
print(null_values)

import pandas as pd
from sklearn.model_selection import train_test_split

# Drop rows with null values
shuffled_df = shuffled_df.dropna()

# Define the features and target variable
X = shuffled_df.drop('Fatigue or not',axis=1)
y = shuffled_df['Fatigue or not']

# Split the data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Display the shapes of the resulting sets
print("Training set shape:", X_train.shape, y_train.shape)
print("Validation set shape:", X_val.shape, y_val.shape)
print("Test set shape:", X_test.shape, y_test.shape)

# Count the occurrences of each unique value in y_test
print("Train data counts: ", y_train.value_counts(),"\n")
print("Val data counts: ", y_val.value_counts(),"\n")
print("Test data counts: ", y_test.value_counts(),"\n")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Create a Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on the training data
rf_model.fit(X_train, y_train)
dump(rf_model, 'body_joint_random_forest_model.joblib')
# Make predictions on the validation set
y_val_pred = rf_model.predict(X_val)

# Evaluate the model's performance on the validation set
validation_accuracy = accuracy_score(y_val, y_val_pred)
validation_report = classification_report(y_val, y_val_pred)

print(f"Validation Set Accuracy: {validation_accuracy}")
print("Validation Set Classification Report:\n", validation_report)

# Make predictions on the test set
y_test_pred = rf_model.predict(X_test)
print("----------------------")
print(y_test_pred)
print("----------------------")

# Evaluate the model's performance on the test set
test_accuracy = accuracy_score(y_test, y_test_pred)
test_report = classification_report(y_test, y_test_pred)

print(f"Test Set Accuracy: {test_accuracy}")
print("Test Set Classification Report:\n", test_report)

# Predict classes and probabilities for test set
test_predictions = rf_model.predict(X_test)
test_probabilities = rf_model.predict_proba(X_test)


# Concatenate X_test and y_test DataFrames
test_data = pd.concat([X_test, y_test], axis=1)
test_data.reset_index(inplace=True)
test_data.head()

test_prob_df = pd.DataFrame(test_probabilities, columns=['non_fatigue', 'fatigue'])
test_prob_df.head()

test_pred_df = pd.DataFrame(test_predictions, columns=['prediction'])
test_pred_df

test_data["predictions"]=test_pred_df['prediction']
test_data["fatigue_index(%)"] = round(test_prob_df["fatigue"]*100,2)
test_data.tail(10)

test_data.drop(['index'],axis=1,inplace=True)
print(test_data.tail(10))

dump(rf_model, 'body_joint_random_forest_model.joblib')