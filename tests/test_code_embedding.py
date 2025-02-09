import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata

@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (["print('Hello, World!')"], [ScriptMetadata(readme_start=0, readme_end=1, path='main.py', content='')])],
        id='one_tagged_script'
    )
def test_code_embedder(readme_content, expected):
    code_embedder = CodeEmbedder(readme_paths=['tests/data/readme.md'], script_path_extractor=ScriptPathExtractor())

    result = code_embedder._read_script_content([ScriptMetadata(readme_start=0, readme_end=1, path='main.py', content='')])    
    assert result == [ScriptMetadata(readme_start=0, readme_end=1, path='main.py', content='print("Hello, World!")\n')]
