from src.script_metadata import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractorInterface

class ScriptMetadataCreator:
    def create(self, start: int, end: int, path: str, extraction_part: str | None = None, content: str = "") -> ScriptMetadata:
        return ScriptMetadata(
            readme_start=start,
            readme_end=end,
            path=path,
            extraction_part=extraction_part,
            content=content,
        )

class ScriptMetadataExtractor(ScriptMetadataExtractorInterface):
    # Existing methods remain the same, but the _finish_current_block method is updated to include content
    def _finish_current_block(self, block: dict, end_row: int, readme_content: list[str]) -> ScriptMetadata:
        content = "\n".join(readme_content[block["start"]+1:end_row])
        return ScriptMetadata(
            readme_start=block["start"],
            readme_end=end_row,
            path=block["path"],
            extraction_part=block["extraction_part"],
            content=content,
        )


In the rewritten code, I have created a `ScriptMetadataCreator` class that handles the creation of `ScriptMetadata` objects. This class has a `create` method that takes the same parameters as the original `create_script_metadata` function, but also includes an additional `content` parameter.

I have also updated the `ScriptMetadataExtractor` class to implement the `ScriptMetadataExtractorInterface` protocol. The `_finish_current_block` method has been updated to include the content of the code block in the `ScriptMetadata` object. This is done by joining the lines of the readme content between the start and end of the code block.