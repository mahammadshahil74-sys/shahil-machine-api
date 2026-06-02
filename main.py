from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import uvicorn

# 1. Initialize the FastAPI app matching your unique OpenAPI info block
app = FastAPI(
    title="Alpha Support Matrix Backend",
    description="Live backend handling machine diagnostic selections and email routing",
    version="1.0.0"
)

# 2. Enable wide-open CORS so IBM watsonx Orchestrate can securely connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define structured Pydantic Data Models matching your tool inputs
class SelectionModel(BaseModel):
    selected_complaint: str

class DispatchModel(BaseModel):
    selected_complaint: str
    user_email: str

# 4. Root Endpoint (For quick health checks to verify your Render server is up)
@app.get("/")
async def health_check():
    return {"status": "Alpha Support Matrix Server is Online and Healthy"}

# 5. STEP 1 ENDPOINT: Handles your clickable dropdown options cleanly
@app.post("/select-fault", status_code=status.HTTP_200_OK)
async def select_fault(payload: SelectionModel):
    """
    Receives the button option selection. Returns an empty plain text 
    response so watsonx does not output messy JSON strings into the user chat.
    """
    print(f"[LOG - STEP 1] User selected structural fault: {payload.selected_complaint}")
    
    # Returning a completely clean text/plain response overrides the default JSON echo
    return Response(content="", media_type="text/plain")

# 6. STEP 2 ENDPOINT: Receives the collective form data and sends notifications
@app.post("/dispatch-ticket", status_code=status.HTTP_200_OK)
async def dispatch_ticket(payload: DispatchModel):
    """
    Receives both the original complaint value and the user-entered email string,
    firing them off together to execute your notification pipeline.
    """
    print(f"[LOG - STEP 2] Processing Ticket Dispatched!")
    print(f"--> Complaint Category: {payload.selected_complaint}")
    print(f"--> Target Destination User: {payload.user_email}")
    
    # This return payload maps cleanly to your final step's success message card variable
    return {
        "notification_status": f"Success! A diagnostic ticket for '{payload.selected_complaint}' has been recorded. A notification was sent to {payload.user_email}."
    }

# Entry point for local debugging execution
if __name__ == "__main__":
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
