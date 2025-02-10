from src.script_metadata import ScriptMetadata

def create_script_metadata(start: int, end: int, path: str, extraction_part: str | None = None, content: str = "") -> ScriptMetadata:
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_part=extraction_part,
        content=content,
    )

I have addressed the feedback from the test case by removing the explanatory comment from the code. I have also added the necessary import statement at the top of the code to ensure that the `ScriptMetadata` class is recognized. I have also ensured that the function definition and type hinting are formatted consistently with the rest of the code.