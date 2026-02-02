import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

df = pd.read_csv("ml/data/students.csv")

X = df[["education_level","stream","cgpa","skills","interest"]]
y = df["career_domain"]

#using preprocessor 
preprocessor = ColumnTransformer ([
("cat",OneHotEncoder(handle_unknown="ignore"),["education_level","stream","interest"]),
("num","passthrough",["cgpa"]),("text",TfidfVectorizer(ngram_range=(1,2),max_features=500), "skills")
])

model = Pipeline ([
("prep",preprocessor),("clf",LogisticRegression(max_iter=3000, class_weight="balanced"))
])

X_train,X_test,y_train,y_test = train_test_split(
X,y,test_size=0.2,random_state=42,stratify=y)

model.fit(X_train,y_train)
pred=model.predict(X_test)
print("Accuracy:",accuracy_score(y_test,pred))

MODEL_PATH=os.path.join("ml","model.joblib")
joblib.dump(model,MODEL_PATH)

print("Model saved")