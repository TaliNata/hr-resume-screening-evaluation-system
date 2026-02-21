from pathlib import Path


class PromptLoader:
    def __init__(self, base_path: str = "prompts", version: str = "v1"):
        self.prompt_dir = Path(base_path) / version

    def load(self, name: str) -> str:
        path = self.prompt_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        return path.read_text(encoding="utf-8")
