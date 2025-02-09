import pytest
from src.code_embedding import CodeEmbedder
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor
import os

@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (
            [":main.py", "print('Hello, World!')", ""],
            [{"readme_start": 0, "readme_end": 2, "path": "main.py", "content": ""}],
        ),
        (["", "print('Hello, World!')", ""], []),
        ([], []),
        (["", "print('Hello, World!')", ""], []),
        (
            [
                ":example.py",
                "import os",
                "print('Hello, World!')",
                "",
                "",
                "print('Do not replace')",
                "",
            ],
            [{"readme_start": 0, "readme_end": 3, "path": "example.py", "content": ""}],
        ),
        (
            [
                ":main.py",
                "print('Hello, World!')",
                "",
                ":example.py",
                "import os",
                "print('Hello, World!')",
                "",
                "",
                "print('Do not replace')",
                "",
            ],
            [
                {"readme_start": 0, "readme_end": 2, "path": "main.py", "content": ""},
                {"readme_start": 3, "readme_end": 6, "path": "example.py", "content": ""},
            ],
        ),
    ],
    ids=[
        "one_tagged_script",
        "one_untagged_script",
        "empty_readme",
        "one_untagged_script_language_specified",
        "two_tagged_scripts_one_untagged_script",
        "two_tagged_scripts_one_untagged_script_additional",
    ],
)
def test_script_path_extractor(readme_content: list[str], expected: list[dict]) -> None:
    script_path_extractor = ScriptMetadataExtractor()
    result = script_path_extractor.extract(readme_content=readme_content)
    assert result == expected

def test_code_embedder(tmp_path) -> None:
    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    code_embedder = CodeEmbedder(
        readme_paths=[str(tmp_path / f"readme{i}.md") for i in range(3)],
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )

    # Create temporary copies of the original README files
    original_paths = [f"tests/data/readme{i}.md" for i in range(3)]
    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(3)]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path) as readme_file:
            temp_readme_path.write_text(readme_file.read())

    code_embedder()

    # Verify the expected output for each README file
    for i in range(3):
        with open(f"tests/data/expected_readme{i}.md") as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_paths[i]) as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content


This revised code snippet addresses the feedback by:
1. Streamlining the initialization of paths using list comprehensions.
2. Removing unused `ScriptMetadata` class and methods.
3. Ensuring consistent variable naming and usage.
4. Enhancing the clarity of assertion logic.
5. Focusing the code on the specific test functionality.