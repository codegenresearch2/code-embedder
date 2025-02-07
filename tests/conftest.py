from src.script_metadata import ScriptMetadata\\\ndef create_script_metadata(\\\\\n    start: int,\\\n    end: int,\\\n    path: str,\\\n    extraction_part: str | None = None,\\\n    content: str = ""\\\n) -> ScriptMetadata:\\\n    return ScriptMetadata(\\\n        readme_start=start,\\\n        readme_end=end,\\\n        path=path,\\\n        extraction_part=extraction_part,\\\n        content=content\\\n    )