import pytest
import os
from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_code_embedder(tmp_path) -> None:
    # Define the original paths explicitly
    original_paths = ["tests/data/readme0.md", "tests/data/readme1.md"]
    expected_paths = ["tests/data/expected_readme0.md", "tests/data/expected_readme1.md"]
    
    # Create temporary copies of the original README files
    temp_readme_paths = [tmp_path / os.path.basename(path) for path in original_paths]
    
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path) as readme_file:
            temp_readme_path.write_text(readme_file.read())

    # Initialize the CodeEmbedder with the temporary paths
    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path) for temp_readme_path in temp_readme_paths],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    # Run the CodeEmbedder
    code_embedder()

    # Read the expected and updated contents for each file
    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path) as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path) as updated_file:
            updated_readme_content = updated_file.readlines()

        # Assert that the updated content matches the expected content
        assert updated_readme_content == expected_readme_content


This revised code snippet addresses the feedback from the oracle by ensuring that all comments are properly prefixed with the `#` symbol, preventing the interpreter from attempting to execute them as code. It also explicitly defines the original and expected paths, uses the `tmp_path` fixture correctly, and includes a return type annotation for the test function.