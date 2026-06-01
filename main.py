from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum

app = FastAPI(
    title="Shahil_Machine_Fault_API",
    description="Generates dropdown options cleanly for Watsonx.",
    version="1.0.0"
)

# Enable CORS so Watsonx can communicate with Render seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

class ComplaintOptions(str, Enum):
    option_1 = "Total Power Failure"
    option_2 = "Overheating Error"
    option_3 = "Mechanical Jam"
    option_4 = "Sensor Calibration Error"

class TicketPayload(BaseModel):
    selected_complaint: ComplaintOptions  

class TicketResponse(BaseModel):
    success_message: str

@app.post(
    "/create-ticket",
    summary="Shahil Custom Ticket Buttons",
    operation_id="Submit_Machine_Fault_Ticket",
    response_model=TicketResponse
)
async def create_ticket(payload: TicketPayload):
    # This prints directly to your Render live console logs when a button is clicked!
    print(f"Option Selected: {payload.selected_complaint.value}")
    
    return {
        "success_message": f"System Fault: {payload.selected_complaint.value}. Details: User reported a {payload.selected_complaint.value.lower()}. Immediate investigation and remediation are recommended."
    }
