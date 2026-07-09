from fastapi.params import Depends
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from src.app.v1.tools.service import ToolsService
from src.core.config import settings
from src.app.v1.ai.schemas import AiResponse

class AiService:
    
    def __init__(self,tools_service: ToolsService = Depends()):
        
        llm = ChatOpenAI(
            model=settings.MODEL,
            temperature=settings.MODEL_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )
        
        currency_tool = StructuredTool.from_function(
            coroutine=tools_service.convert_currencies,
            name="convert_currencies",
            description=tools_service.convert_currencies.__doc__
        )
        
        self.tools = [currency_tool]

        self.agent_executor = create_react_agent(
            model=llm,
            tools=self.tools,
            prompt=settings.OPENAI_SYSTEM_PROMPT
        )

     

    async def execute_openai(self, enquiry: str) -> AiResponse:
        try:
            inputs = {"messages": [("human", enquiry)]}
            response = await self.agent_executor.ainvoke(inputs)
            final_message = response["messages"][-1].content
            return AiResponse(message=final_message)

        except Exception as e:
            print(f"[OpenaiService] Error executing OpenAI request: {str(e)}")
            raise RuntimeError(f"OpenAI API Failure: {str(e)}")