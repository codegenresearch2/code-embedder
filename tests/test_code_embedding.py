import pytest
from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_code_embedder(tmp_path):
    # List of original README file paths
    original_paths = ["tests/data/readme0.md", "tests/data/readme1.md", "tests/data/readme2.md"]
    # List of expected README file paths
    expected_paths = ["tests/data/expected_readme0.md", "tests/data/expected_readme1.md", "tests/data/expected_readme2.md"]

    # Ensure all original files exist
    for original_path in original_paths:
        if not tmp_path.joinpath(original_path).exists():
            raise FileNotFoundError(f"The file {original_path} does not exist.")

    # Instantiate CodeEmbedder with necessary components
    code_embedder = CodeEmbedder(
        readme_paths=[str(tmp_path / original_path) for original_path in original_paths],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader()
    )

    # Run the embedding process
    code_embedder()

    # Compare the updated readme content with the expected content
    for original_path, expected_path in zip(original_paths, expected_paths):
        updated_readme_content = tmp_path.joinpath(original_path).read_text().splitlines()
        expected_readme_content = open(expected_path).read().splitlines()
        assert updated_readme_content == expected_readme_content