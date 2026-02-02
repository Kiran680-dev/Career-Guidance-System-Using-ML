import joblib

# Load model and vectorizer
model = joblib.load("ml/skill_model.joblib")
vectorizer = joblib.load("ml/skill_vectorizer.joblib")

def predict_career_from_skills(skill_list):
    # Convert list into single string
    skills_text = " ".join(skill_list).lower()
    # Vectorize
    skills_vectorized = vectorizer.transform([skills_text])
    # Predict
    prediction = model.predict(skills_vectorized)
    return prediction[0]