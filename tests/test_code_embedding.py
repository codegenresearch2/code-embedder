import pytest

from src.code_embedding import CodeEmbedder
from src.script_metadata import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

class CodeEmbedder:
    def __init__(self, readme_paths, script_metadata_extractor, script_content_reader):
        self.readme_paths = readme_paths
        self.script_metadata_extractor = script_metadata_extractor
        self.script_content_reader = script_content_reader

    def embed_scripts(self):
        for readme_path in self.readme_paths:
            with open(readme_path, 'r') as file:
                readme_content = file.readlines()

            scripts = self.script_metadata_extractor.extract(readme_content)
            for script in scripts:
                script.content = self.script_content_reader.read(script.path)
                readme_content[script.readme_start:script.readme_end] = [script.content]

            with open(readme_path, 'w') as file:
                file.writelines(readme_content)

def test_code_embedder(tmp_path) -> None:
    original_paths = [
        "tests/data/readme0.md",
        "tests/data/readme1.md",
        "tests/data/readme2.md",
    ]
    expected_paths = [
        "tests/data/expected_readme0.md",
        "tests/data/expected_readme1.md",
        "tests/data/expected_readme2.md",
    ]

    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path) as readme_file:
            temp_readme_path.write_text(readme_file.read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path) for temp_readme_path in temp_readme_paths],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    code_embedder.embed_scripts()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path) as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path) as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content