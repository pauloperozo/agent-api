from langchain_openai import ChatOpenAI
from src.core.config import settings
from langchain_core.messages import HumanMessage
from src.app.v1.ai.schemas import AiResponse

class AiService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )

    async def execute_openai(self, enquiry: str) -> AiResponse:
        try:

            messages = [HumanMessage(content=enquiry)]
            response = await self.llm.ainvoke(messages)
            return AiResponse(message=response.content)

        except Exception as e:
            print(f"[OpenaiService] Error executing OpenAI request: {str(e)}")
            raise RuntimeError(f"OpenAI API Failure: {str(e)}")