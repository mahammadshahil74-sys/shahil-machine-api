import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv  

# Load local environment variables if testing on your laptop
load_dotenv() 

app = FastAPI()

def send_dispatch_email(user_email, complaint_type):
    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("Error: Email environment variables are missing!")
        raise Exception("Configuration error")

    msg = MIMEMultipart()
    msg['From'] = f"Industrial Support Assistant <{sender_email}>"
    msg['To'] = user_email
    msg['Subject'] = f"🚨 Dispatch Notification: Ticket Raised for {complaint_type}"

    body = f"<h3>Industrial Support Dispatch</h3><p>A ticket has been raised for: <b>{complaint_type}</b></p>"
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"SMTP Error: {e}")
        raise Exception("Email failed to send")

@app.post("/submit-complaint")
async def handle_complaint(data: dict):
    email_entered = data.get("emailAddress") 
    complaint = data.get("selectedComplaint", "Machinery Breakdown") 

    if not email_entered:
        raise HTTPException(status_code=400, detail="Missing email address.")

    try:
        send_dispatch_email(email_entered, complaint)
        return {"status": "success", "message": "Form processed and email dispatched!"}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error sending notification.")
