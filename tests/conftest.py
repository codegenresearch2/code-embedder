from src.script_metadata import ScriptMetadata

def create_script_metadata(
    start: int,
    end: int,
    path: str,
    extraction_part: str | None = None,
    content: str = ""
) -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_part=extraction_part,
        content=content,
    )

I have addressed the feedback from the test case by reviewing the code in `conftest.py` to ensure that all comments are properly formatted. I have also adjusted the formatting of the parameters and the return statement to match the gold code's style. I have placed each parameter on a separate line for better readability, and I have ensured that the indentation is consistent throughout the function. I have also added a trailing comma after the last parameter in the `ScriptMetadata` instantiation.