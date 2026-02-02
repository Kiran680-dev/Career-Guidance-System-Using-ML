import joblib
import pandas as pd
import numpy as np
import os

# base directory and model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")

# Load the trained pipeline 
model = joblib.load(MODEL_PATH)
def predict_career(stream, cgpa, education_level, skills, interest):
    try:
        input_df = pd.DataFrame([{
        "education_level":education_level,
        "stream":stream,
        "cgpa":cgpa,
        "skills":skills,
        "interest":interest
    }])
        prediction = model.predict(input_df)[0]
        # Confidence Score
        probabilities = model.predict_proba(input_df)

        probs = probabilities[0]
        top_prob = np.max(probs)

        #confidance smoothing 
        confidence = round((top_prob * 0.85 + 0.15) * 100,2)
        confidence=min(confidence,95)

        return prediction, confidence
    except Exception as e:
        return f"Error: {str(e)}", 0