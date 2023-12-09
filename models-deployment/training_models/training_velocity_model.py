import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

# Load the data
fatigue = pd.read_csv("velocity_model_fatigue_detection_csv_data/processed_fatigue_data.csv")
non_fatigue = pd.read_csv("velocity_model_fatigue_detection_csv_data/processed_nonfatigue_data.csv")

# Concatenate fatigue and non-fatigue data
data = pd.concat([fatigue, non_fatigue], ignore_index=True)

# Shuffle the dataset
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Drop unnecessary columns
data.drop(['Period_Start', 'Period_End', 'Velocity_abs'], axis=1, inplace=True)

# Define features and target variable
X = data.drop('Fatigue or not', axis=1)
y = data['Fatigue or not']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create Random Forest classifier
rf_classifier = RandomForestClassifier(random_state=42)

# Define the parameter grid for grid search
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

# Perform grid search with 5-fold cross-validation
grid_search = GridSearchCV(estimator=rf_classifier, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best parameters and the corresponding accuracy
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print("Best Parameters:", best_params)
print("Best Accuracy:", best_score)

# Train the model with the best parameters on the entire training set
best_rf_classifier = RandomForestClassifier(**best_params, random_state=42)
best_rf_classifier.fit(X_train, y_train)

# Save the trained model to a file
dump(best_rf_classifier, 'velocity_model_random_forest_model.joblib')

# Evaluate the model on the test set
test_predictions = best_rf_classifier.predict(X_test)
test_accuracy = accuracy_score(y_test, test_predictions)
print(f"\nTest Accuracy: {test_accuracy:.4f}\n")
print("Classification Report for Test Set:")
print(classification_report(y_test, test_predictions))

# Process the test data for later analysis
test_probabilities = best_rf_classifier.predict_proba(X_test)
test_data = pd.concat([X_test, y_test], axis=1)
test_data.reset_index(inplace=True, drop=True)
test_data["predictions"] = test_predictions
test_data["fatigue_index(%)"] = round(pd.DataFrame(test_probabilities, columns=['non_fatigue', 'fatigue'])["fatigue"] * 100, 2)

# Display the last few rows of processed test data
print(test_data.tail(10))
