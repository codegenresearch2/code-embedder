from src.script_metadata import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor

class ScriptMetadataCreator:
    def __init__(self, extractor: ScriptMetadataExtractor):
        self.extractor = extractor

    def create(self, readme_content: list[str]) -> list[ScriptMetadata]:
        scripts = self.extractor.extract(readme_content)
        for script in scripts:
            script.content = self._extract_content(readme_content, script)
        return scripts

    def _extract_content(self, readme_content: list[str], script: ScriptMetadata) -> str:
        return '\n'.join(readme_content[script.readme_start + 1: script.readme_end])


In this rewrite, I've created a new class `ScriptMetadataCreator` that takes an instance of `ScriptMetadataExtractor` as a dependency. This allows for better modularization and separation of concerns. The `create` method now uses the extractor to get the initial metadata, and then it fills in the `content` field for each `ScriptMetadata` object. The `_extract_content` method is a helper method that extracts the content from the readme based on the start and end indices.