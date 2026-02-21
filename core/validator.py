import json
from jsonschema import validate, ValidationError
from pathlib import Path


class SchemaValidator:
    def __init__(self, schema_path: str):
        self.schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))

    def validate(self, data: dict):
        try:
            validate(instance=data, schema=self.schema)
        except ValidationError as e:
            raise ValueError(f"Schema validation error: {e.message}")
