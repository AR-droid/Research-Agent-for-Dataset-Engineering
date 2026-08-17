import logging
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)

class AgentExecutionError(Exception):
    """Exception raised for errors during agent execution."""
    pass

class BaseAgent(Generic[InputType, OutputType]):
    def __init__(
        self,
        name: str,
        input_schema: Type[InputType],
        output_schema: Type[OutputType],
        system_instructions: str,
        allowed_tools: Optional[Dict[str, Callable]] = None,
        timeout_seconds: int = 60,
        max_retries: int = 3,
        model_name: str = "gemini-3.5-flash"
    ):
        self.name = name
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.system_instructions = system_instructions
        self.allowed_tools = allowed_tools or {}
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.execution_state: Dict[str, Any] = {}
        self.logger = logging.getLogger(self.name)
        
        # Initialize Langchain Gemini Model
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.2,
            max_retries=max_retries,
            timeout=timeout_seconds,
        ).with_structured_output(self.output_schema)

    def sanitize_untrusted_content(self, content: str) -> str:
        """
        Prompt injection defense: Sanitize and wrap untrusted content.
        This explicitly wraps retrieved content in <UNTRUSTED_CONTENT> tags
        so the LLM can differentiate between system instructions and external data.
        """
        sanitized = content.replace("<UNTRUSTED_CONTENT>", "").replace("</UNTRUSTED_CONTENT>", "")
        return f"<UNTRUSTED_CONTENT>\n{sanitized}\n</UNTRUSTED_CONTENT>"

    def execute(self, input_data: InputType) -> OutputType:
        """
        Execute the agent logic with the given input data via LangChain.
        """
        self.execution_state['status'] = 'running'
        self.execution_state['input'] = input_data.model_dump()
        
        retries = 0
        while retries <= self.max_retries:
            try:
                self.logger.info(f"[{self.name}] Executing run attempt {retries + 1}...")
                
                messages = [
                    SystemMessage(content=self.system_instructions),
                    HumanMessage(content=f"Input: {input_data.model_dump_json()}\nAvailable Tools: {list(self.allowed_tools.keys())}")
                ]
                
                # Execute Langchain invocation with structured output
                result = self.llm.invoke(messages)
                
                if not isinstance(result, self.output_schema):
                    raise ValueError(f"Expected {self.output_schema.__name__}, got {type(result)}")
                
                self.execution_state['status'] = 'completed'
                return result

            except Exception as e:
                self.logger.warning(f"[{self.name}] Execution error on attempt {retries + 1}: {e}")
                retries += 1
                if retries > self.max_retries:
                    self.logger.error(f"Execution failed permanently: {e}")
                    self.execution_state['status'] = 'failed'
                    self.execution_state['error'] = str(e)
                    raise AgentExecutionError(f"Agent {self.name} failed after {self.max_retries} retries: {e}") from e

        self.execution_state['status'] = 'failed'
        raise AgentExecutionError(f"Agent {self.name} failed.")
