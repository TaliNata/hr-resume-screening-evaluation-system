from core.prompt_loader import PromptLoader
from core.llm_client import LLMClient
from core.validator import SchemaValidator
from core.evaluator import Evaluator
import json


class HRScreeningPipeline:
    """
    Pipeline for HR resume screening using LLMs.
    Handles prompt loading, input/output validation, LLM generation, and evaluation.
    """
    
    def __init__(self, prompt_version="v1", llm_temperature=0.0, input_schema_path="schemas/input_schema.json", output_schema_path="schemas/output_schema.json"):
        """
        Initializes the pipeline with configurable parameters.
        
        Args:
            prompt_version (str): Version of prompts to load.
            llm_temperature (float): Temperature for LLM clients.
            input_schema_path (str): Path to input schema JSON.
            output_schema_path (str): Path to output schema JSON.
        """
        loader = PromptLoader(version=prompt_version)
        self.system_prompt = loader.load("system.txt")
        self.role_prompt = loader.load("role.txt")
        self.instructions_prompt = loader.load("instructions.txt")
        self.evaluation_prompt = loader.load("evaluation.txt")

        self.llm = LLMClient(temperature=llm_temperature)
        # Using separate LLM for evaluation to allow different configs if needed
        self.evaluator_llm = LLMClient(temperature=llm_temperature)

        self.input_validator = SchemaValidator(input_schema_path)
        self.output_validator = SchemaValidator(output_schema_path)

        self.evaluator = Evaluator(self.evaluator_llm, self.evaluation_prompt)

    def run(self, input_data: dict) -> dict:
        """
        Runs the screening pipeline on the provided input data.
        
        Args:
            input_data (dict): Input data to process, must be JSON-serializable.
            
        Returns:
            dict: Dictionary with 'result' and 'evaluation' keys.
            
        Raises:
            ValueError: If input_data is not JSON-serializable or validation fails.
            RuntimeError: If LLM generation or evaluation fails.
        """
        try:
            # Validate input
            self.input_validator.validate(input_data)
            
            # Ensure input_data is JSON-serializable
            json.dumps(input_data)
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": self.role_prompt},
                {"role": "user", "content": self.instructions_prompt},
                {"role": "user", "content": json.dumps(input_data)}
            ]
            
            llm_output = self.llm.generate(messages)
            self.output_validator.validate(llm_output)
            
            evaluation = self.evaluator.evaluate(llm_output)
            
            return {
                "result": llm_output,
                "evaluation": evaluation
            }
        except json.JSONDecodeError:
            raise ValueError("Input data is not JSON-serializable.")
        except Exception as e:
            raise RuntimeError(f"Pipeline execution failed: {str(e)}")
        # TODO: Add unit tests with mocked LLMs for better reliability.
        # TODO: Consider async handling or caching for high-volume use to improve performance.