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

I have addressed the feedback from the test case by removing the explanatory comment from the `conftest.py` file. I have also formatted the function definition to match the gold code's style by placing each parameter on a new line for better readability. I have ensured that the indentation of the parameters and the return statement is consistent with the gold code. The type hinting for `extraction_part` is already formatted consistently with the rest of the code.