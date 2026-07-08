from pydantic import BaseModel, Field

class AiResponse(BaseModel):
    message: str = Field(
        ..., 
        example="La rºespuesta del asistente a la consulta del usuario."
    )