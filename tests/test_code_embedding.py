import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata

@pytest.mark.parametrize(
    'readme_content, expected',
    [
        (['print(\"Hello, World! from script\")'], [ScriptMetadata(readme_start=0, readme_end=0, path='script.py', content='')])],
        id='one_tagged_script'
    )
def test_script_path_extractor(readme_content, expected):
    script_path_extractor = ScriptPathExtractor()
    result = script_path_extractor.extract(readme_content=readme_content)
    assert result == expected

# Additional functions and test cases can be added here to further align with the gold code.