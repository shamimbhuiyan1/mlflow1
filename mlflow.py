import pandas as pd

# Load dataset
data = pd.read_csv('train.csv')  # Replace 'train.csv' with your uploaded file's name
print(data.head())

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Drop rows with missing values
data = data.dropna()

# Encode categorical variables
encoder = LabelEncoder()
for column in ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status', 'Dependents']:  # Added 'Dependents' here
    data[column] = encoder.fit_transform(data[column])

# Define features (X) and target (y)
X = data.drop(['Loan_ID', 'Loan_Status'], axis=1)
y = data['Loan_Status']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Start an MLflow run
with mlflow.start_run():
    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Log model and metrics in MLflow
    mlflow.sklearn.log_model(model, "loan_model")
    mlflow.log_metric("accuracy", accuracy)

    print(f"Model logged with accuracy: {accuracy}")
