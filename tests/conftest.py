from src.script_metadata import ScriptMetadata

def create_script_metadata(start: int, end: int, path: str, extraction_part: str | None = None, content: str = "") -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_part=extraction_part,
        content=content,
    )

I have addressed the feedback from the test case by reviewing and correcting the code in `conftest.py` to ensure that all string literals are properly terminated with matching quotation marks. I have also adjusted the formatting of the parameters to match the gold code's style by placing them on a single line, separated by commas. I have ensured that the indentation of the parameters and the return statement is consistent with the gold code. I have also reviewed the overall structure of the function to ensure it matches the gold code's style.