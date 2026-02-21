from core.prompt_loader import PromptLoader
from core.llm_client import LLMClient
from core.validator import SchemaValidator
from core.evaluator import Evaluator
import json


class HRScreeningPipeline:
    def __init__(self):
        loader = PromptLoader(version="v1")
        self.system_prompt = loader.load("system.txt")
        self.role_prompt = loader.load("role.txt")
        self.instructions_prompt = loader.load("instructions.txt")
        self.evaluation_prompt = loader.load("evaluation.txt")

        self.llm = LLMClient(temperature=0.0)
        self.evaluator_llm = LLMClient(temperature=0.0)

        self.input_validator = SchemaValidator("schemas/input_schema.json")
        self.output_validator = SchemaValidator("schemas/output_schema.json")

        self.evaluator = Evaluator(self.evaluator_llm, self.evaluation_prompt)

    def run(self, input_data: dict) -> dict:
        # 1. Validate input
        self.input_validator.validate(input_data)

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
