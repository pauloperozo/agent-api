from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.core.config import settings
from src.app.v1.ai.schemas import AiResponse

class AiService:
    
    def __init__(self):
        llm = ChatOpenAI(
            model=settings.MODEL,
            temperature=settings.MODEL_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", settings.OPENAI_SYSTEM_PROMPT),
            ("human", "{enquiry}")
        ])

        self.chain = prompt | llm 

    async def execute_openai(self, enquiry: str) -> AiResponse:
        try:
            response = await self.chain.ainvoke({"enquiry": enquiry})
            return AiResponse(message=response.content)

        except Exception as e:
            print(f"[OpenaiService] Error executing OpenAI request: {str(e)}")
            raise RuntimeError(f"OpenAI API Failure: {str(e)}")