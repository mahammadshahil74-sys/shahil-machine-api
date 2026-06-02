import os
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv  

load_dotenv() 

app = FastAPI()

def send_dispatch_email(user_email, complaint_type):
    sender_email = os.environ.get("SENDER_EMAIL")
    api_key = os.environ.get("SENDGRID_API_KEY")

    if not sender_email or not api_key:
        print("Error: SendGrid API credentials are missing from Render!")
        raise Exception("Configuration error")

    # Pure HTTPS web endpoint—Render never blocks this!
    url = "https://api.sendgrid.com/v3/mail/send"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "personalizations": [{
            "to": [{"email": user_email}]
        }],
        "from": {
            "email": sender_email,
            "name": "Industrial Support Assistant"
        },
        "subject": f"🚨 Dispatch Notification: Ticket Raised for {complaint_type}",
        "content": [{
            "type": "text/html",
            "value": f"<h3>Industrial Support Dispatch</h3><p>A ticket has been raised for: <b>{complaint_type}</b></p>"
        }]
    }

    try:
        print("Attempting to send email via SendGrid Web API...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code not in [200, 201, 202]:
            print(f"SendGrid API Error: {response.text}")
            raise Exception(f"SendGrid rejected mail: {response.status_code}")
        print(f"Success: Dispatch email sent cleanly via Web API to {user_email}")
    except Exception as e:
        print(f"Web API Delivery Error: {e}")
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
        raise HTTPException(status_code=500, detail=str(e))
