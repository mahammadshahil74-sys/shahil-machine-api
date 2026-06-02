import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv  

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

# --- BOTH ROUTES NOW REDIRECT HERE SO IT NEVER 404s ---

@app.post("/select-fault")
@app.post("/submit-complaint")
async def handle_complaint(data: dict):
    # Print incoming data to the logs so you can see it live
    print(f"Incoming Watsonx Data: {data}")

    # Fallback checks to match any variations in your JSON setup keys
    email_entered = data.get("emailAddress") or data.get("email")
    complaint = data.get("selectedComplaint") or data.get("faultType") or "Machinery Breakdown"

    if not email_entered:
        # If watsonx hits it during an initial schema validation pass, don't crash
        return {"status": "success", "message": "Endpoint active, awaiting data pass."}

    try:
        send_dispatch_email(email_entered, complaint)
        return {"status": "success", "message": "Form processed and email dispatched!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email system error: {str(e)}")
