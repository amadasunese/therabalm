from flask import Flask, render_template, request, redirect, url_for, flash
from jinja2 import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'assessment development'

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'therabalms@gmail.com'
app.config["MAIL_PASSWORD"] = 'oxoz gqyw nfcj bnul'

# Initialize Flask-Mail
mail = Mail(app)

# Initialize some variables to hold user data temporarily (not recommended in production)
user_data = {}

# Define the list of questions
questions = [
    "Do you often find it difficult to fall asleep?",
    "Do you get extremely sweaty palms when you have a big event ahead?",
    "Do you find it difficult to speak with your loved ones about situations you are experiencing?",
    "Do you feel irritated when people ask you basic questions about yourself?",
    "Do you experience a sudden change of emotions which cannot be explained?",
    "Do you often feel like you are not good enough?",
    "Is maintaining long-term interest in things a difficulty for you?",
    "Do you feel a sense of emptiness whenever you are alone?",
    "Have you ever taken medications to help calm your nerves?",
    "Do you feel like you sleep too much?",
    "Do you feel restless and tired even after a long night of rest?",
    "Do you have frequent outbursts of anger that you eventually regret?"
]

@app.route('/assessment')
def assessment():
    # Enumerate the questions with their corresponding indices
    enumerated_questions = list(enumerate(questions))
    return render_template('assessment.html', enumerated_questions=enumerated_questions)


@app.route('/process_question', methods=['POST'])
def process_question():
    score = 0

    for i, question in enumerate(questions):
        answer = request.form.get(f'answer_{i}')
        if answer == 'yes':
            score += 1

    if score >= 1:
        return redirect(url_for('book_appointment'))
    else:
        return redirect(url_for('faq'))

@app.route('/faq')
def faq():
    # You can render an FAQ page here or redirect to external FAQ links.
    return render_template('faq.html')

@app.route('/book_appointment')
def book_appointment():
    return render_template('appointment.html')

@app.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    appointment_data = {
        'name': request.form.get('name'),
        'gender': request.form.get('gender'),
        'phone': request.form.get('phone'),
        'email': request.form.get('email'),
        'age': request.form.get('age'),
        'city': request.form.get('city'),
        'state': request.form.get('state'),
        'country': request.form.get('country'),
        'message': request.form.get('message'),
        'preferred_days': request.form.get('preferred_days'),
        'preferred_time': request.form.get('preferred_time')
    }

    # Send appointment details to the therapist
    send_email(appointment_data, 'therabalms@gmail.com', 'Appointment Request')

    # Send a confirmation email to the user
    send_email_confirmation(appointment_data, request.form.get('email'))

    # Store user's appointment data temporarily (not recommended in production)
    user_data['appointment'] = appointment_data

    flash('Appointment submitted successfully. You will receive a confirmation email.')
    return redirect(url_for('confirmation'))

def send_email(appointment_data, recipient_email, subject):
    try:
        msg = Message(subject=subject,
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[recipient_email])

        # Format the email body with appointment details
        body = f"Name: {appointment_data['name']}\n" \
               f"Gender: {appointment_data['gender']}\n" \
                f"Phone: {appointment_data['phone']}\n" \
                    f"Email Address: {appointment_data['email']}\n" \
                        f"Age: {appointment_data['age']} years old\nCity/Town: {appointment_data['city']}, " \
                            f"State: {appointment_data['state']}\n"\
                                f"Message: {appointment_data['message']}\n"\
                                    f"Preferred Days of Appointment: {appointment_data['preferred_days']}\n"\
                                        f"Preferred Time of Appointment: {appointment_data['preferred_time']} "


               # Include other appointment details here

        msg.body = body

        # Send the email
        mail.send(msg)

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_email_confirmation(appointment_data, user_email):
    # Compose and send a confirmation email to the user (similar to the therapist email)
    send_email(appointment_data, user_email, 'Appointment Confirmation')

@app.route('/confirmation')
def confirmation():
    appointment_data = user_data.get('appointment', {})
    return render_template('confirmation.html', appointment_data=appointment_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app.route('/selfassessment')
def selfassessment():
    return render_template('selfassessment.html')
    
app.static_folder = 'static'

if __name__ == '__main__':
    app.run(debug=True)
