import pytest
from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_code_embedder(tmp_path):
    # Create a temporary copy of the original readme file
    original_path = "tests/data/readme.md"
    temp_readme_path = tmp_path / "readme.md"
    temp_readme_path.write_text(open(original_path).read())

    # Instantiate CodeEmbedder with necessary components
    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path)],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader()
    )

    # Run the embedding process
    code_embedder()

    # Read the updated readme file
    updated_readme_content = temp_readme_path.read_text()

    # Compare the updated readme content with the expected content
    expected_readme_content = open("tests/data/expected_readme.md").read()
    assert updated_readme_content == expected_readme_content