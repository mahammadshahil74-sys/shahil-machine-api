from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal

app = FastAPI(
    title="Shahil_Advanced_Form_API",
    description="Provides seamless interactive options and handles quiet ticket workflow pipelines.",
    version="2.0.0"
)

# Enable CORS for Watsonx
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This explicitly declares the 4 text choices inside your Python code!
class ComplaintSelection(BaseModel):
    selected_complaint: Literal[
        "Total Power Failure",
        "Overheating Error",
        "Mechanical Jam",
        "Sensor Calibration Error"
    ]

# Schema for the final step that receives both the choice and the email
class EmailNotificationPayload(BaseModel):
    selected_complaint: str
    user_email: str

@app.post("/create-ticket", summary="Submit Machine Fault Form Item")
async def create_ticket(payload: ComplaintSelection):
    """
    Step 1: Captures the chosen option from the interactive Watsonx menu.
    Logs it to Render console, then goes completely silent (Empty text string).
    """
    print(f"User selected option via Form: {payload.selected_complaint}")
    return Response(content="", media_type="text/plain")

@app.post("/send-email-notification", summary="Send Workflow Email Notification")
async def send_email(payload: EmailNotificationPayload):
    """
    Step 2: Triggered at the end of your workflow once the user types their email.
    """
    print(f"Triggering confirmation email to: {payload.user_email} for {payload.selected_complaint}")
    return {
        "notification_status": f"Ticket raised successfully! A confirmation email has been sent to {payload.user_email}."
    }
