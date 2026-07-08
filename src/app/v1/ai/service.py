from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.config import settings
from langchain_core.messages import HumanMessage
from src.app.v1.ai.schemas import AiResponse

class AiService:
    
    def __init__(self):
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", settings.OPENAI_SYSTEM_PROMPT),
            ("human", "{enquiry}")
        ])

        self.chain = prompt | llm | StrOutputParser()

    async def execute_openai(self, enquiry: str) -> AiResponse:
        try:
            response = await self.chain.ainvoke({"enquiry": enquiry})
            return AiResponse(message=response)

        except Exception as e:
            print(f"[OpenaiService] Error executing OpenAI request: {str(e)}")
            raise RuntimeError(f"OpenAI API Failure: {str(e)}")