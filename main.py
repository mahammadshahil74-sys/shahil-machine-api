from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI(
    title="Shahil_Machine_Fault_API",
    description="Generates dropdown options cleanly for Watsonx.",
    version="1.0.0"
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
    print(f"Option Selected: {payload.selected_complaint.value}")
    return {
        "success_message": f"**Ticket raised successfully for: {payload.selected_complaint.value}!**"
    }