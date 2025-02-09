import pytest\"nfrom src.code_embedding import CodeEmbedder, ScriptContentReader, ScriptMetadataExtractor\"nimport os\"n\"n@pytest.fixture\"ndef create_temp_copy(tmp_path):\"n    original_paths = ['tests/data/readme0.md', 'tests/data/readme1.md', 'tests/data/readme2.md']\"n    temp_readme_paths = [tmp_path / f'readme{i}.md' for i in range(len(original_paths))]\"n    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):\"n        with open(original_path) as readme_file:\"n            temp_readme_path.write_text(readme_file.read())\"n    return temp_readme_paths\"n\"ndef test_code_embedder(tmp_path) -> None:\"n    code_embedder = CodeEmbedder(\"n        readme_paths=[str(tmp_path / f'readme{i}.md') for i in range(3)], \"n        script_path_extractor=ScriptPathExtractor(), \"n        script_metadata_extractor=ScriptMetadataExtractor(), \"n        script_content_reader=ScriptContentReader()\"n    )\"n    code_embedder()\"n    expected_paths = ['tests/data/expected_readme0.md', 'tests/data/expected_readme1.md', 'tests/data/expected_readme2.md']\"n    for i, expected_path in enumerate(expected_paths):\"n        with open(expected_path) as expected_file:\"n            expected_readme_content = expected_file.readlines()\"n        with open(tmp_path / f'readme{i}.md') as updated_file:\"n            updated_readme_content = updated_file.readlines()\"n        assert expected_readme_content == updated_readme_content\"n