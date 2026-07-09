from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from src.core.config import settings
from src.app.v1.tools.service import ToolsService

def create_agent(tools_service: ToolsService) -> any:

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

    tools = [currency_tool]

    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=settings.OPENAI_SYSTEM_PROMPT
    )

def format_agent_input(enquiry: str) -> dict:
    return {"messages": [("human", enquiry)]}

def parse_agent_output(response: dict) -> str:
    return response["messages"][-1].content