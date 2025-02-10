# Updated create_script_metadata function
def create_script_metadata(
    start: int, end: int, path: str, extraction_part: str | None = None, content: str = ""
) -> ScriptMetadata:
    # Ensure that all comments and code are properly formatted
    # Remove any descriptive text that is not valid Python syntax
    # Ensure that any multi-line comments are properly initiated and terminated
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_part=extraction_part,
        content=content,
    )