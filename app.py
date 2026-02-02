#env variables
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

#flask core
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify
)

#auth 
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.linkedin import make_linkedin_blueprint

#Security
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

#dictionary
from career_data import career_info, career_details

#Database
from models import (
    get_conn,
    create_user,
    get_user_by_email,
    save_prediction,
    save_skill_prediction,
    save_feedback,
    save_contact
)

#ML module
from ml.predict import predict_career
from ml.skill_predict import predict_career_from_skills

#other 
import pandas as pd
import re
from datetime import timedelta

#email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

csrf = CSRFProtect(app)

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email",
           "https://www.googleapis.com/auth/userinfo.profile"]
)

app.register_blueprint(google_bp, url_prefix="/login")

#linkedin Oauth
from flask_dance.contrib.linkedin import make_linkedin_blueprint, linkedin

linkedin_bp = make_linkedin_blueprint(
    client_id=os.getenv("LINKEDIN_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("LINKEDIN_OAUTH_CLIENT_SECRET"),
    scope="openid profile email"
)

app.register_blueprint(linkedin_bp, url_prefix="/login")
# Session lifetime
app.permanent_session_lifetime = timedelta(minutes=30)

# Secure Cookie Settings
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  

serializer = URLSafeTimedSerializer(app.secret_key)

def send_reset_email(to_email, reset_url):
    try:
        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=to_email,
            subject="Password Reset Request",
            html_content=f"""
            <h2>Password Reset</h2>
            <p>You requested to reset your password.</p>
            <a href="{reset_url}"
               style="background:#6c63ff;padding:10px 20px;
               color:white;text-decoration:none;border-radius:5px;">
               Reset Password
            </a>
            <p>This link expires in 10 minutes.</p>
            """
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print("Email Sent! Status:", response.status_code)

    except Exception:
        import traceback
        traceback.print_exc()


# Home Page
@app.route("/")
def home():
    return render_template("base.html")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("signup"))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format!", "error")
            return redirect(url_for("signup"))

        existing = get_user_by_email(email)
        if existing:
            flash("Email already registered. Please login.", "error")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)
        create_user(name, email, password_hash)

        flash(f"Signup successful for {name}! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signUp.html")

# Prediction Page
@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("login"))
    
    if request.method == "GET":
        try:
            df = pd.read_csv("ml/data/students.csv")
            streams = sorted(df["stream"].unique())
            education_levels = sorted(df["education_level"].unique())

        except Exception:
            streams = ["Commerce", "Arts", "Science", ]
            education_levels = ["Undergraduate", "Postgraduate"]
        return render_template("Predict.html", streams=streams, education_levels=education_levels)

    name = request.form.get("name")
    education_level = request.form.get("education_level")
    stream = request.form.get("stream")
    cgpa_raw = request.form.get("cgpa", "0")
    
    skills = request.form.get("skills")
    interest = request.form.get("interest")

    print("Form Data:", name, education_level, stream, cgpa_raw, skills, interest)

    if education_level == "Select Education Level" or stream == "Select Stream":
        flash("Please select valid Education Level and Stream.", "error")
        return redirect(url_for("prediction"))

    try:
        cgpa = float(cgpa_raw)
    except ValueError:
        flash("Invalid CGPA value.", "error")
        return redirect(url_for("prediction"))

    try:
        career, confidence = predict_career(
            stream=stream,
            cgpa=cgpa,
            education_level=education_level,
            skills=skills,
            interest=interest
        )
        
        print("Predicted Career:", career)
    except Exception as e:
        flash(f"Prediction error: {e}", "error")
        return redirect(url_for("prediction"))

    try:
        save_prediction(name, education_level, stream, cgpa, skills, interest, career)
        print("Saved to DB")

    except Exception as e:
        print("Database error:", e)

    info = career_details.get(career,{
    "description":"No description available",
    "suggestion":"Explore learning resources related to this career."
    })

    return render_template(
    "result.html", 
    name=name,
    career=career,
    stream=stream,
    cgpa=cgpa,
    education_level=education_level,
    confidence=confidence,
    description=info["description"],
    suggestion=info["suggestion"]
    )

#discover yourself prediction 
@app.route("/discover_predict", methods=["POST"])
def discover_predict():

    skill1 = request.form.get("skill1", "")
    skill2 = request.form.get("skill2", "")
    skill3 = request.form.get("skill3", "")
    skill4 = request.form.get("skill4", "")
    skill5 = request.form.get("skill5", "")

    skills = [skill1, skill2, skill3, skill4, skill5]
    skills = [s for s in skills if s.strip() != ""]

    print("Skills Received:", skills)

    if not skills:
        return render_template("discover.html", career="Please enter at least one skill.")

    career = predict_career_from_skills(skills)
    
    info = career_info.get(career,{
    "description":"No description available",
    "suggestion":"Explore learning resources related to this career.",
    "courses":[]
    })
    
    print("Predicted Career:", career)

    # Save prediction in database
    try:
        save_skill_prediction(skills, career)
        print("Skill prediction saved")
    except Exception as e:
        print("DB error:", e)
                         
                         
    return render_template(
       "result2.html",
       career=career,
       description=info["description"],
       suggestion=info["suggestion"],
       courses=info["courses"]
    )

#google Login route 
@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")

    if not resp.ok:
        flash("Failed to fetch user info from Google", "error")
        return redirect(url_for("login"))

    user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name")

    user = get_user_by_email(email)

    if not user:
        random_password = os.urandom(16).hex()
        create_user(name, email, generate_password_hash(random_password))

    user = get_user_by_email(email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    flash("Google login successful!", "success")
    return redirect(url_for("home"))

#login OAuth Route 
@app.route("/linkedin_login")
def linkedin_login():
    if not linkedin.authorized:
        return redirect(url_for("linkedin.login"))

    resp = linkedin.get("userinfo")

    if not resp.ok:
        flash("Failed to fetch user info from LinkedIn", "error")
        return redirect(url_for("login"))

    user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name")

    user = get_user_by_email(email)

    if not user:
        create_user(name, email, generate_password_hash("linkedin_user"))

    user = get_user_by_email(email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    flash("LinkedIn login successful!", "success")
    return redirect(url_for("home"))

# Other Routes
@app.route("/predict")
def predict():
    return render_template("beforePredict.html")

@app.route("/discover")
def discover():
    return render_template("discover.html", career=None)

@app.route("/courses")
def courses():
    return render_template("course_details.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "login_attempts" not in session:
        session["login_attempts"] = 0

    if request.method == "POST":
        # brute force protection
        if session["login_attempts"] >= 5:
            flash("Too many login attempts. Please try again later.", "error")
            return redirect(url_for("login"))

        email = request.form.get("email")
        password = request.form.get("password")

        # basic email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format!", "error")
            return redirect(url_for("login"))

        user = get_user_by_email(email)

        if user and check_password_hash(user["password_hash"], password):
            session["login_attempts"] = 0

            if request.form.get("remember"):
                session.permanent = True
            else:
                session.permanent = False

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Login successful!", "success")
            return redirect(url_for("home"))

        else:
            session["login_attempts"] += 1
            flash("Invalid email or password!", "error")

    return render_template("login.html", page_type="login")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", page_type="logout")


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        rating = request.form.get("rating")
        message = request.form.get("message")

        save_feedback(rating, message)
        flash("Thank you for your feedback!", "success")
        return redirect(url_for("feedback_success"))

    return render_template("feedback.html")


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    save_contact(name, email, message)
    flash("Message sent successfully!", "success")
    return redirect(url_for("home"))

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form.get("email")
        user = get_user_by_email(email)

        if user:
            token = serializer.dumps(email, salt="password-reset-salt")
            reset_url = url_for("reset_password", token=token, _external=True)
            send_reset_email(email, reset_url)

        flash("If this email is registered, a reset link has been sent.", "success")
        return redirect(url_for("forgot"))

    return render_template("forgotpassword.html")

@app.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=600)
    except:
        flash("Reset link expired or invalid!", "error")
        return redirect(url_for("forgot"))

    if request.method == "POST":
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(request.url)

        password_hash = generate_password_hash(new_password)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password_hash=%s WHERE email=%s",
                    (password_hash, email))
        conn.commit()
        cur.close()
        conn.close()

        flash("Password updated successfully!", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/feedback_success")
def feedback_success():
    return render_template("success.html")

@app.route("/course/<name>")
def course_page(name):
    conn = get_conn()
    cur = conn.cursor(dictionary=True, buffered=True)

    cur.execute("SELECT id FROM courses WHERE course_name=%s", (name,))
    course = cur.fetchone()

    if course and "user_id" in session:
        cur.execute(
            "INSERT INTO course_views (user_id, course_id) VALUES (%s,%s)",
            (session["user_id"], course["id"])
        )
        conn.commit()

    cur.close()
    conn.close()

    template_name = f"{name}.html"

    if os.path.exists(os.path.join(app.template_folder, template_name)):
        return render_template(template_name)

    flash("Course page not found")
    return redirect(url_for("courses"))    

@app.route("/admin/add_course", methods=["POST"])
def add_course():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor()

    course_name = request.form["course_name"]
    description = request.form["description"]

    cur.execute(
        "INSERT INTO courses (course_name, short_description) VALUES (%s,%s)",
        (course_name, description)
    )

    conn.commit()
    cur.close()
    conn.close()
    flash("Course added successfully")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete_course/<int:id>")
def delete_course(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Course deleted")
    return redirect(url_for("admin_dashboard"))


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # check admin role
    cur.execute("SELECT role FROM users WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()

    if user["role"] != "admin":
        flash("Access denied")
        return redirect(url_for("home"))

    # fetch data
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM feedback")
    feedbacks = cur.fetchall()

    cur.execute("SELECT * FROM contact_messages")
    contacts = cur.fetchall()

    cur.execute("SELECT * FROM career_predictions")
    predictions = cur.fetchall()
    
    cur.execute("SELECT * FROM skill_predictions")
    skill_predictions = cur.fetchall()
    
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    cur.execute("""
        SELECT courses.course_name, COUNT(course_views.id) AS total_views
        FROM courses
        LEFT JOIN course_views ON courses.id = course_views.course_id
        GROUP BY courses.id
    """)

    course_analytics = cur.fetchall()

    cur.close()
    conn.close()
    
    return render_template(
    "admin_dashboard.html",
    users=users,
    feedbacks=feedbacks,
    contacts=contacts,
    predictions=predictions,
    skill_predictions=skill_predictions,
    courses=courses,
    course_analytics=course_analytics
    )

# Run the App
if __name__ == "__main__":
    app.run(debug=False)