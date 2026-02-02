import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

#signup
def create_user(name, email, password_hash):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, password_hash))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def save_prediction(name, education_level, stream, cgpa, skills,
                    interest, predicted_career):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    INSERT INTO career_predictions 
    (name, education_level, stream, cgpa, skills, interest, predicted_career)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    
    cur.execute(sql, (name, education_level, stream, cgpa, skills, interest, predicted_career))
    
    conn.commit()
    cur.close()
    conn.close()


#feedback
def save_feedback(rating, message):
    conn = get_conn()
    cur = conn.cursor()
    sql = "INSERT INTO feedback (rating, message) VALUES (%s, %s)"
    cur.execute(sql, (rating, message))
    conn.commit()
    cur.close()
    conn.close()

#Contact Save
def save_contact(name, email, message):
    conn = get_conn()
    cur = conn.cursor()
    sql = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
    cur.execute(sql, (name, email, message))
    conn.commit()
    cur.close()
    conn.close()

#save ml model prediction code   
def save_skill_prediction(skills, predicted_career):
    conn = get_conn()
    cur = conn.cursor()
    skills_text = ", ".join(skills)
    sql = """
    INSERT INTO skill_predictions
    (skills, predicted_career)
    VALUES (%s,%s)
    """
    cur.execute(sql, (skills_text, predicted_career))
    conn.commit()
    cur.close()
    conn.close()