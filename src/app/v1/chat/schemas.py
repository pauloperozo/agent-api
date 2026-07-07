from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    enquiry: str = Field(
        ...,
        description="The natural language query or question from the user for the assistant.",
        example="Cuantos Son 900 USD en peso colombianos?"
    )

class ChatResponse(BaseModel):
    message: str = Field(
        ..., 
        example="La rºespuesta del asistente a la consulta del usuario."
    )