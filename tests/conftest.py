from src.script_metadata import ScriptMetadata

def create_script_metadata(
    readme_start: int,
    readme_end: int,
    path: str,
    extraction_part: str | None = None,
    content: str = ""
) -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=readme_start,
        readme_end=readme_end,
        path=path,
        extraction_part=extraction_part,
        content=content
    )