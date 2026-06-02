from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Alpha_Support_Matrix_Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SelectionModel(BaseModel):
    selected_complaint: str

class DispatchModel(BaseModel):
    selected_complaint: str
    user_email: str

@app.post("/select-fault")
async def select_fault(payload: SelectionModel):
    """
    Step 1: Quietly logs the selected button option without sending chat text back.
    """
    print(f"Alpha Log - Fault Selection: {payload.selected_complaint}")
    return Response(content="", media_type="text/plain")

@app.post("/dispatch-ticket")
async def dispatch_ticket(payload: DispatchModel):
    """
    Step 2: Receives the user email from the canvas form and triggers confirmation message.
    """
    print(f"Alpha Log - Dispatched to: {payload.user_email}")
    return {
        "notification_status": f"Ticket raised successfully! A confirmation email has been sent to {payload.user_email}."
    }
