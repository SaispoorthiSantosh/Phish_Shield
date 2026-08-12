import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
import joblib

# Load dataset
data = pd.read_csv("dataset/Phishing_Email.csv")

# Remove empty emails
data = data.dropna(subset=["Email Text", "Email Type"])
data = data.reset_index(drop=True)

# Remove extra column if present
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"])

# Convert labels
data["Email Type"] = data["Email Type"].map({
    "Safe Email": 0,
    "Phishing Email": 1
})

# Features and labels
X = data["Email Text"]
y = data["Email Type"]

# Convert text into numerical features
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Machine Learning model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Calculate performance
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Display results
print("\n===================================")
print("       PHISHSHIELD MODEL RESULTS")
print("===================================")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")

print("\nConfusion Matrix:")
print(cm)

print("\n===================================")

# Save model
joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\nModel trained and saved successfully!")