class Evaluator:
    def __init__(self, llm_client, evaluation_prompt: str):
        self.llm = llm_client
        self.evaluation_prompt = evaluation_prompt

    def evaluate(self, llm_output: dict) -> dict:
        messages = [
            {
                "role": "system",
                "content": self.evaluation_prompt
            },
            {
                "role": "user",
                "content": str(llm_output)
            }
        ]

        return self.llm.generate(messages)
