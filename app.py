from flask import Flask, render_template, request, session, redirect, url_for
from ai_engine import InterviewEngine

app = Flask(__name__)
app.secret_key = "mockmate_secret_key_2026"

engine = InterviewEngine()


# ------------------------------
# HOME
# ------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ------------------------------
# SETUP PAGE
# ------------------------------

@app.route("/setup")
def setup():
    return render_template("setup.html")

@app.route("/about")
def about():
    return render_template("about.html")
# ------------------------------
# START INTERVIEW
# ------------------------------

@app.route("/interview", methods=["POST"])
def interview():

    role = request.form["role"]
    company = request.form.get("company", "")
    difficulty = request.form["difficulty"]
    duration = request.form["duration"]

    # Decide total questions
    if duration == "15":
        total_questions = 5
    elif duration == "30":
        total_questions = 10
    else:
        total_questions = 15

    # Store interview information
    session["role"] = role
    session["company"] = company
    session["difficulty"] = difficulty
    session["duration"] = duration
    session["current_question"] = 1
    session["total_questions"] = total_questions
    session["history"] = []

    # Generate first question
    question = engine.generate_first_question(
        role,
        company,
        difficulty
    )

    # Save first question
    history = session["history"]

    history.append({
        "question": question,
        "answer": ""
    })

    session["history"] = history

    # Progress bar percentage
    progress = (
        session["current_question"]
        / session["total_questions"]
    ) * 100

    return render_template(
        "interview.html",
        role=role,
        company=company,
        difficulty=difficulty,
        duration=duration,
        question=question,
        current_question=session["current_question"],
        total_questions=session["total_questions"],
        progress=progress
    )


# ------------------------------
# NEXT QUESTION
# ------------------------------

@app.route("/next_question", methods=["POST"])
def next_question():

    answer = request.form["answer"]

    history = session["history"]

    # Save answer to previous question
    history[-1]["answer"] = answer

    session["history"] = history

    role = session["role"]
    company = session["company"]
    difficulty = session["difficulty"]

    current_question = session["current_question"]
    total_questions = session["total_questions"]

    # Interview Finished
    if current_question >= total_questions:

        report = engine.generate_report(
            role,
            company,
            difficulty,
            history
        )

        return render_template(
            "report.html",
            report=report,
            role=role,
            company=company,
            difficulty=difficulty,
            total_questions=total_questions
        )

    # Generate next question
    question = engine.generate_next_question(
        role,
        company,
        difficulty,
        history
    )

    # Save next question
    history.append({
        "question": question,
        "answer": ""
    })

    session["history"] = history

    # Increase question number
    session["current_question"] += 1

    # Progress percentage
    progress = (
        session["current_question"]
        / session["total_questions"]
    ) * 100

    return render_template(
        "interview.html",
        role=role,
        company=company,
        difficulty=difficulty,
        duration=session["duration"],
        question=question,
        current_question=session["current_question"],
        total_questions=session["total_questions"],
        progress=progress
    )


# ------------------------------
# RESET INTERVIEW
# ------------------------------

@app.route("/reset")
def reset():

    session.clear()

    return redirect(url_for("home"))


# ------------------------------
# RUN APP
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)