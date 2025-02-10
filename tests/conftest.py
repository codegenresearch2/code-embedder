from src.script_metadata import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractorInterface

class ScriptMetadataCreator:
    def create(self, start: int, end: int, path: str, extraction_part: str | None = None) -> ScriptMetadata:
        return ScriptMetadata(
            readme_start=start,
            readme_end=end,
            path=path,
            extraction_part=extraction_part,
            content="",
        )

class ScriptMetadataCreatorInterface(Protocol):
    def create(self, start: int, end: int, path: str, extraction_part: str | None = None) -> ScriptMetadata: ...


In the rewritten code, I have created a `ScriptMetadataCreator` class that has a `create` method to create a `ScriptMetadata` object. I have also created an interface `ScriptMetadataCreatorInterface` for better abstraction and flexibility. This allows for the easy swapping of different implementations of the `ScriptMetadataCreator` class. The `create` method now takes in the necessary parameters and returns a `ScriptMetadata` object. This improves the readability and maintainability of the code by separating the responsibilities into different classes.