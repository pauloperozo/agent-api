from fastapi import Depends
from src.app.v1.tools.service import ToolsService
from src.app.v1.ai.schemas import AiResponse
from src.app.v1.ai.agent import (
    create_agent,
    format_agent_input,
    parse_agent_output
)


class AiService:
    
    def __init__(self,tools_service: ToolsService = Depends()):
        self.agent_executor = create_agent(tools_service)
    
    async def execute_openai(self, enquiry: str) -> AiResponse:
        try:
            inputs = format_agent_input(enquiry)
            response = await self.agent_executor.ainvoke(inputs)
            message = parse_agent_output(response)
            return AiResponse(message=message)

        except Exception as e:
            print(f"[OpenaiService] Error executing OpenAI request: {str(e)}")
            raise RuntimeError(f"OpenAI API Failure: {str(e)}")