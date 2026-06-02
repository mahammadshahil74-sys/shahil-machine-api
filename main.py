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
        print("Error: Email environment variables are missing from Render!")
        raise Exception("Configuration error")

    msg = MIMEMultipart()
    msg['From'] = f"Industrial Support Assistant <{sender_email}>"
    msg['To'] = user_email
    msg['Subject'] = f"🚨 Dispatch Notification: Ticket Raised for {complaint_type}"

    body = f"<h3>Industrial Support Dispatch</h3><p>A ticket has been raised for: <b>{complaint_type}</b></p>"
    msg.attach(MIMEText(body, 'html'))

    # FIXED: Using direct SSL on Port 465 with an explicit 10-second timeout to prevent hanging
    try:
        print("Attempting connection to secure Gmail SMTP server...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
        print(f"Success: Dispatch email sent cleanly to {user_email}")
    except Exception as e:
        print(f"SMTP Connection Error: {e}")
        raise Exception(f"Mail delivery service failed: {str(e)}")

@app.post("/select-fault")
@app.post("/submit-complaint")
@app.post("/dispatch-ticket")
async def handle_complaint(data: dict):
    print(f"Incoming Watsonx Data: {data}")

    email_entered = (
        data.get("user_email") or 
        data.get("emailAddress") or 
        data.get("email")
    )
    
    complaint = (
        data.get("selected_complaint") or 
        data.get("selectedComplaint") or 
        data.get("faultType") or 
        "Machinery Breakdown"
    )

    if not email_entered:
        print("Step 1 data cached. Waiting for user email input step...")
        return {
            "status": "success", 
            "message": f"Fault selected: {complaint}. Awaiting email step."
        }

    try:
        send_dispatch_email(email_entered, complaint)
        return {
            "status": "success", 
            "message": "Form processed completely and dispatch email sent!"
        }
    except Exception as e:
        # Returns a clean message back to watsonx instead of locking the UI
        raise HTTPException(status_code=500, detail=str(e))
