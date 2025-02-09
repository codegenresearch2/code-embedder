import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor

@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (["print('Hello, World!')"], [ScriptMetadata(readme_start=0, readme_end=1, path='main.py', content='')])],
    ids=['one_tagged_script']
)
def test_code_embedder(readme_content, expected):
    code_embedder = CodeEmbedder(
        readme_paths=['tests/data/readme.md'],
        script_path_extractor=ScriptPathExtractor(),
        script_content_reader=ScriptContentReader(),
        script_metadata_extractor=ScriptMetadataExtractor()
    )

    result = code_embedder._read_script_content(
        scripts=[ScriptMetadata(readme_start=0, readme_end=1, path='main.py', content='')]
    )
    assert result == [ScriptMetadata(readme_start=0, readme_end=1, path='main.py', content='print("Hello, World!")\n')]
