import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("ml/data/skill_data.csv")

# Features and Labels
X = df["skills"]
y = df["career"]

# Convert text → numbers
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vectorized, y)

# Save model + vectorizer
joblib.dump(model, "ml/skill_model.joblib")
joblib.dump(vectorizer, "ml/skill_vectorizer.joblib")

print("Skill Model Trained Successfully :)")