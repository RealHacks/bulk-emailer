from flask import Flask, request, render_template, redirect, flash
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form.get("subject")
        message = request.form.get("message")
        recipients = request.form.get("recipients").split(",")

        try:
            send_bulk_email(subject, message, recipients)
            flash("Emails sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send emails: {str(e)}", "danger")

        return redirect("/")

    return render_template("index.html")

def send_bulk_email(subject, message, recipients):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = recipient.strip()
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))
            server.sendmail(EMAIL_ADDRESS, recipient.strip(), msg.as_string())

if __name__ == "__main__":
    app.run(debug=True)