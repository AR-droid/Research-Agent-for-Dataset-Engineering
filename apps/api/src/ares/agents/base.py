import logging
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError

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
        max_retries: int = 3
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

    def sanitize_untrusted_content(self, content: str) -> str:
        """
        Prompt injection defense: Sanitize and wrap untrusted content.
        This explicitly wraps retrieved content in <UNTRUSTED_CONTENT> tags
        so the LLM can differentiate between system instructions and external data.
        """
        # Remove any existing tags that could be used for injection
        sanitized = content.replace("<UNTRUSTED_CONTENT>", "").replace("</UNTRUSTED_CONTENT>", "")
        return f"<UNTRUSTED_CONTENT>\n{sanitized}\n</UNTRUSTED_CONTENT>"

    def mock_llm_call(self, prompt: str) -> str:
        """
        Mock implementation of an LLM API call.
        In a real implementation, this would call OpenAI, Anthropic, or similar.
        """
        self.logger.info(f"[{self.name}] Calling mock LLM...")
        return "{}"

    def execute(self, input_data: InputType) -> OutputType:
        """
        Execute the agent logic with the given input data.
        """
        self.execution_state['status'] = 'running'
        self.execution_state['input'] = input_data.model_dump()
        
        retries = 0
        while retries <= self.max_retries:
            try:
                # 1. Prepare prompt
                prompt = self._prepare_prompt(input_data)
                
                # 2. Call LLM (mocked here, in reality might involve tool calls loop and timeout management)
                raw_output = self.mock_llm_call(prompt)
                
                # 3. Parse output (dummy empty JSON for mock, normally we'd parse the LLM JSON response)
                mocked_output = self._generate_mock_output()
                
                # 4. Validate output against output schema
                validated_output = self.output_schema(**mocked_output)
                self.execution_state['status'] = 'completed'
                return validated_output

            except ValidationError as e:
                self.logger.warning(f"Validation error on attempt {retries + 1}: {e}")
                retries += 1
            except Exception as e:
                self.logger.error(f"Execution error: {e}")
                self.execution_state['status'] = 'failed'
                self.execution_state['error'] = str(e)
                raise AgentExecutionError(f"Agent {self.name} failed: {e}") from e

        self.execution_state['status'] = 'failed'
        raise AgentExecutionError(f"Agent {self.name} failed after {self.max_retries} retries.")

    def _prepare_prompt(self, input_data: InputType) -> str:
        prompt = f"System: {self.system_instructions}\n"
        prompt += f"Input: {input_data.model_dump_json()}\n"
        prompt += f"Available Tools: {list(self.allowed_tools.keys())}\n"
        return prompt

    def _generate_mock_output(self) -> Dict[str, Any]:
        """Generate a mock dictionary that passes the output_schema validation."""
        mock_data = {}
        for field_name, field in self.output_schema.model_fields.items():
            if "List" in str(field.annotation):
                mock_data[field_name] = []
            elif "Dict" in str(field.annotation):
                mock_data[field_name] = {}
            elif "bool" in str(field.annotation):
                mock_data[field_name] = True
            elif "float" in str(field.annotation):
                mock_data[field_name] = 1.0
            elif "int" in str(field.annotation):
                mock_data[field_name] = 1
            else:
                mock_data[field_name] = "mock_value"
        return mock_data
