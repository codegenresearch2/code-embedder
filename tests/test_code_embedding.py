import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor
import os

@pytest.mark.parametrize(
    'readme_content, expected',
    [
        (['print("Hello, World! from script")'], [ScriptMetadata(readme_start=0, readme_end=0, path='script.py', content='')])
    ],
    ids=['one_tagged_script']
)
def test_extract_script_metadata(readme_content, expected, tmp_path):
    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    code_embedder = CodeEmbedder(
        readme_paths=[os.path.join(tmp_path, 'readme.md')],
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader
    )

    # Create a temporary copy of the README file
    readme_path = os.path.join(tmp_path, 'readme.md')
    with open(readme_path, 'w') as readme_file:
        readme_file.writelines(readme_content)

    result = code_embedder._read_script_content([
        ScriptMetadata(readme_start=0, readme_end=0, path='script.py', content='')]
    )
    assert result == expected