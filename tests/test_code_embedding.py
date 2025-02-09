import pytest
import shutil
from pathlib import Path
from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_code_embedder(tmp_path):
    # List of original README file paths
    original_paths = ["tests/data/readme0.md", "tests/data/readme1.md", "tests/data/readme2.md"]
    # List of expected README file paths
    expected_paths = ["tests/data/expected_readme0.md", "tests/data/expected_readme1.md", "tests/data/expected_readme2.md"]

    # Create temporary copies of the original README files
    for original_path in original_paths:
        original_file_path = Path(original_path)
        if not original_file_path.exists():
            raise FileNotFoundError(f"The file {original_path} does not exist.")
        shutil.copy(original_file_path, tmp_path / original_file_path.name)

    # Instantiate CodeEmbedder with necessary components
    code_embedder = CodeEmbedder(
        readme_paths=[tmp_path / original_path.name for original_path in Path(original_paths[0]).glob('*.md')],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader()
    )

    # Run the embedding process
    code_embedder()

    # Compare the updated readme content with the expected content
    for expected_path in expected_paths:
        expected_readme_content = open(expected_path).readlines()
        updated_readme_content = (tmp_path / Path(expected_path).name).read_text().splitlines()
        assert updated_readme_content == expected_readme_content