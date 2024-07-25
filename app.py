from flask import Flask, flash, render_template, request, redirect, url_for, session 

app = Flask(__name__)
app.secret_key = '123-456-789'

# Define a survey for demonstration
survey = {
    "title": "Customer Satisfaction Survey",
    "description": "Please fill out a survey about your experience with us.",
    "questions": [
        "Have you shopped here before?",
        "Did someone else shop with you today?",
        "On average, how much do you spend a month on frisbees?",
        "Are you likely to shop here again?"
    ],
    "choices": [
        ["Yes", "No"],
        ["Yes", "No"],
        ["Less than $10,000", "$10,000 or more"],
        ["Yes", "No"]
    ]
}

responses = []

@app.route('/')
def index():
    return render_template('index.html', survey=survey)

@app.route('/start_survey', methods=["POST"])
def start_survey():
    session['responses'] = []  # Initialize session responses
    return redirect(url_for('question', qid=0))

@app.route('/questions/<int:qid>', methods=["GET", "POST"])
def question(qid):
    # Check if the user has already answered all questions
    if len(responses) >= len(survey['questions']):
        return redirect(url_for('thank_you'))

    # Check if the question ID is valid
    if qid < 0 or qid >= len(survey['questions']):
        flash("Invalid question ID. Redirecting to the first unanswered question.")
        return redirect(url_for('index'))

    # Check if the user is trying to access a question they should not
    if qid > len(responses):
        flash("You must answer previous questions before accessing this one.")
        return redirect(url_for('question', qid=len(responses)))

    if request.method == "POST":
        answer = request.form.get('answer')
        if not answer:
            return "No answer provided", 400  # Bad Request
        responses.append(answer)
        next_qid = qid + 1
        if next_qid >= len(survey['questions']):
            return redirect(url_for('thank_you'))
        else:
            return redirect(url_for('question', qid=next_qid))
    
    if qid >= len(survey['questions']):
        return redirect(url_for('index'))
    
    question_text = survey['questions'][qid]
    choices = survey['choices'][qid]
    return render_template('question.html', qid=qid, question=question_text, choices=choices, survey=survey)

@app.route('/thank_you')
def thank_you():
    return "Thank you for completing the survey!"

@app.route('/responses')
def view_responses():
    return render_template('responses.html', responses=responses, survey=survey)

if __name__ == '__main__':
    app.run(debug=True)
